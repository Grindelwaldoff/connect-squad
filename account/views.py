from django.http import HttpResponse
from django.views.generic.edit import UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, forms
from django.contrib.auth.decorators import login_required

from account.models import Profile
from account.forms import (
    UserRegistrationForm,
    LoginForm, EmailChangeForm,
    ProfileEditForm
)
from shop.models import Category, Product


User = get_user_model()


@login_required
def dashboard(request):
    return render(
        request,
        'account/dashboard.html',
        {'section': 'dashboard'}
    )


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd['username'],
                password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(
        request,
        'account/login.html',
        {'form': form, 'title': 'login'}
    )


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(
                request,
                'account/register_done.html',
                {'new_user': new_user}
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'account/register.html',
        {'user_form': user_form, 'title': 'register'}
    )


@login_required
def edit(request):
    product = Product.objects.filter(seller=request.user.id)
    user = get_object_or_404(User, username=request.user)
    password_form = forms.PasswordChangeForm(user)
    email_form = EmailChangeForm(user)
    if request.method == 'POST':
        if 'password_change' in request.POST:
            password_form = forms.PasswordChangeForm(
                user,
                data=request.POST,
            )
            if password_form.is_valid():
                password_form.save()
                return redirect('inpage:index')
        if 'email_change' in request.POST:
            email_form = EmailChangeForm(
                instance=user,
                data=request.POST
            )
            print('check')
            if email_form.is_valid():
                print('check1')
                email_form.save()
                return redirect('inpage:index')
    return render(
        request,
        'account/edit.html',
        {
            'email_change': email_form,
            'password_change': password_form,
            'title': 'Profile',
            'telegram': product.filter(category=4),
            'instagram': product.filter(category=5),
            'vk': product.filter(category=2),
            'ok': product.filter(category=3),
            'whatsapp': product.filter(category=6)
        }
    )
