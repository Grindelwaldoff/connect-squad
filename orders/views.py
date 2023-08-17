from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from account.models import Payment
from shop.models import HistoryByAccountGroup
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.core.files import File

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})


@login_required
def order_history(request):
    try:
        histors = HistoryByAccountGroup.objects.filter(user=request.user)
    except:
        histors = None

    return render(request, 'orders/history/historybasket.html', {'histors': histors, 'title': 'Basket'})


@login_required
def order_history_down(request,id):
    try:
        histors = HistoryByAccountGroup.objects.filter(id=id,user=request.user)

        archive_path = f"archive/tg/{histors[0]}"
        with open(archive_path, 'rb') as f:
            file = File(f)
            response = HttpResponse(file, content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{histors[0]}"'
            return response
    except Exception as E:
        pass
    try:
        histors = HistoryByAccountGroup.objects.filter(user=request.user)
    except:
        histors = None

    return render(request, 'orders/history/historybasket.html', {'histors': histors,'title': 'Basket'})

@login_required
def refill(request):
    if request.method == 'POST':
        add_balance = request.POST.get('add-balance-input')
        request.user.profile.increase_balance(int(add_balance))
    __res = Payment.objects.filter(user=request.user)

    return render(request, 'orders/balance/refill.html',{'hist': __res, 'title': 'Balance'})