import shutil
import zipfile

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.files import File

from cart.forms import CartAddProductForm
from shop.models import Category, Product, AccountGroup, HistoryByAccountGroup
from inpage.models import Advertisement
from .filters import GeneralFilter


@login_required
def buy_product(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)

        account_group = AccountGroup.objects.filter(
            product=product
        ).order_by('-id').first()
    except Exception as E:
        print(E)
        return redirect(reverse(
            'shop:product_list_by_category',
            kwargs={'category_slug': 'telegram'}
        ))
    if request.user.profile.deduct_balance(product.price):

        product.stock -= 1
        product.save()
        account_n = account_group.account_name
        archive_path = f'account_{account_n}_{product.stock}.zip'

        with zipfile.ZipFile(archive_path, 'w') as zip_file:
            zip_file.write(str(account_group.torrent_file), arcname=account_n)

        with open(archive_path, 'rb') as f:
            file = File(f)

            response = HttpResponse(file, content_type='application/zip')
            response['Content-Disposition'] = ('attachment; '
                                               f'filename="{account_n}.zip"')
        next_path = f"archive/tg/{archive_path}"
        shutil.copyfile(archive_path, next_path)
        cats = Category.objects.get(name='Telegram')
        history = HistoryByAccountGroup(
            user=request.user,
            category=cats,
            account_name=account_n,
            torrent_file=next_path
        )
        history.save()
        account_group.delete()
        return response
    else:
        return redirect(reverse(
            'shop:product_list_by_category',
            kwargs={'category_slug': 'telegram'}
        ))


def product_list(request, category_slug=None):
    template = settings.LINKS[category_slug]
    filter = GeneralFilter(
        request.GET,
        queryset=Product.objects.filter(category__slug=category_slug)
    )
    # Реклама
    try:
        adv = Advertisement.objects.get(active=True)
    except Exception:
        adv = None
    return render(
        request,
        template,
        {
            'title': category_slug,
            'filter': filter,
            'countries': settings.COUNTRY_CHOICES,
            'adv': adv
        }
    )


def product_detail(request, slug):
    product = get_object_or_404(Product,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(
        request,
        'shop/product/detail.html',
        {'product': product,
         'cart_product_form': cart_product_form,
         'title': 'telegram'}
    )


@login_required
def update_product_detail(request, slug):
    product = get_object_or_404(
        Product, slug=slug
    )
    new_params = {
        'price': request.POST.get('form_new_price'),  # тестовое название поля
        'description': request.POST.get('form_new_desc'),  # тестовое название поля
        'name': request.POST.get('form_new_name')  # тестовое название поля
    }
    for param, value in new_params.items():
        if value is not None:
            setattr(Product, param, value)
    product.save()
    return redirect('shop:product_detail')


# def product_del(request, slug):
#     product = get_object_or_404(Product, slug=slug)
#     product.slug = 'dsflgkjsdfgd'
#     product.save()
#     return redirect(
#         'edit'
#     )


# def product_set_active(request, slug, active):
#     product = get_object_or_404(Product, slug=slug)
#     product.is_active = not(active)
#     product.save()
#     return redirect(
#         'edit'
#     )
