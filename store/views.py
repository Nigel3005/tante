from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
import os
from django.template import RequestContext
from store import urls
from django.urls import path, include
from django.core.mail import send_mail
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)


# Create your views here.
def login_View(request):
    if request.method == 'POST' and 'login' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/shop')
            else:
                data = {
                    'error': 'User account not activated',
                }
                return render(request, 'registration-shop/login-shop.html', data)
        else:
            data = {
                'error': 'Incorrect password and/or username',
            }
            return render(request, 'registration-shop/login-shop.html', data)

    data = {
        'error': '',
    }

    return render(request, 'registration-shop/login-shop.html', data)


def logoutView(request):
    logout(request)
    return redirect('shop')


def handler404(request, *args, **argv):
    if request.get_full_path != f"{path}":
        data = {
            'page': 'store/404.html',
        }
        return render(request, 'store/main.html', data)


def store_View(request):
    context = {}
    # data = {
    #     'page': 'store/store.html',
    #     'context': context,
    # }
    return render(request, 'store/store.html', context)


def cart_View(request):
    context = {}
    # data = {
    #     'page': 'store/cart.html',
    #     'context': context,
    # }
    return render(request, 'store/cart.html', context)



def checkout_View(request):
    context = {}
    # data = {
    #     'page': 'store/checkout.html',
    #     'context': context,
    # }
    return render(request, 'store/checkout.html', context)

