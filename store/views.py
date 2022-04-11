import datetime
import json
import os.path

from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)
from django.shortcuts import redirect
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .forms import SignUpForm, ProductForm
from .models import *
from .utils import cartData, guestOrder


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


def register_View(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration-shop/register-shop.html', {'form': form})


def makeMailUserService(name, mail, sub, msg):
    data = {'name': name, 'mail': mail, 'sub': sub, 'msg': msg}
    MSG = '''
Webmail van:    {}
Mail adres :    {}
Message: 
{}
    '''.format(data['name'], data['mail'], data['msg'])
    contactForm = contact(name=name, email=mail, bericht=msg)
    contactForm.save()

    send_mail(data['sub'], MSG, 'webmail@user-service.nl', ['info@user-service.nl'],
              fail_silently=False, auth_user='webmail@user-service.nl', auth_password='N@na2548NDW!')


def makeMailClient(mail):
    MSG = '''
Bedankt voor het invullen van ons contact formulier! Hierbij is bevestigd dat
wij uw mail ontvangen hebben. Wij zullen zo spoedig mogelijk contact met
u opnemen!
Vriendelijke groet,
User Service
'''
    send_mail('Bevestiging WebForm User-Service', MSG, 'noreply@user-service.nl', [mail],
              fail_silently=False, auth_user='noreply@user-service.nl', auth_password='N@na2548NDW!')


def contactView(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        bericht = request.POST.get('bericht')
        makeMailUserService(name, email, 'Contactformulier User Service', bericht)
        makeMailClient(email)

        data = {
            'name': name,
        }
        return render(request, 'store/contact-correct.html', data)

    else:
        return render(request, 'store/contact.html')


def logoutView(request):
    logout(request)
    return redirect('/')


def handler404(request, *args):
    if request.get_full_path != f"{path}":
        data = {
            'page': 'store/404.html',
        }
        return render(request, 'store/main.html', data)


def store_View(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'order': order, 'items': items}
    return render(request, 'store/store.html', context)


def product_View(request, id):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    cartContext = {'items': items, 'order': order, 'cartItems': cartItems}
    context = dict()
    # add the dictionary during initialization
    context["product"] = Product.objects.get(id=id)
    print(id)

    args = {
        'product': Product.objects.get(id=id),
    }
    return render(request, 'store/product_view.html', args, cartContext)


def cart_View(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout_View(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        print('User is not logged in')
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    print('Total matches')
    print(total)
    order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            postcode=data['shipping']['postcode'],
            stad=data['shipping']['stad'],
            nummer=data['shipping']['nummer'],
        )

    return JsonResponse('Payment submitted..', safe=False)


def orders_View(request):
    if request.user.is_superuser:
        orders = Order.objects.all().order_by('id').reverse()
        orderItems = OrderItem.objects.all()
        context = {'orders': orders, 'orderItems': orderItems}
        print('authenticated superuser')

        return render(request, 'store/order.html', context)
    else:
        print('not authenticated')
        return redirect('/')


def dashboard_View(request):
    if request.user.is_superuser:
        products = Product.objects.all()
        customers = Customer.objects.all()
        orders = Order.objects.all().order_by('id').reverse()
        orderItems = OrderItem.objects.all()
        context = {'orders': orders, 'orderItems': orderItems, 'products': products, 'customers': customers}
        return render(request, 'store/dashboard.html', context)
    else:
        print('not authenticated')
        return redirect('/')


# CRUD PRODUCTS

def create_view(request):
    if request.user.is_superuser:
        # dictionary for initial data with
        # field names as keys

        context = dict()
        # add the dictionary during initialization
        form = ProductForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard?ecom=2')

        context['form'] = form

        data = {
            'form': ProductForm(request.POST or None),
        }

        return render(request, 'store/dashboard.html', data)
    else:
        print('not authenticated')
        return redirect('/')


def list_view(request):
    if request.user.is_superuser:
        # dictionary for initial data with
        # field names as keys
        context = dict()

        # add the dictionary during initialization
        context["products"] = Product.objects.all()

        data = {
            'products': Product.objects.all(),
        }

        return render(request, 'store/dashboard.html', data)
    else:
        print('not authenticated')
        return redirect('/')


# pass id attribute from urls
def detail_view(request, id):
    if request.user.is_superuser:
        # dictionary for initial data with
        # field names as keys
        context = dict()
        print('detail view')
        # add the dictionary during initialization
        context["product"] = Product.objects.get(id=id)
        print(id)

        args = {
            'product': Product.objects.get(id=id),
        }

        return render(request, "store/dashboard.html", args)
    else:
        print('not authenticated')
        return redirect('/')


# update view for details
def update_view(request, id):
    if request.user.is_superuser:
        # dictionary for initial data with
        # field names as keys
        context = dict()
        print('update view')

        # fetch the object related to passed id
        obj = get_object_or_404(Product, id=id)
        # pass the object as instance in form

        form = ProductForm(request.POST or None, request.FILES or None, instance=obj)

        # save the data from the form and
        # redirect to detail_view
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/dashboard/" + str(id))

        # add form dictionary to context
        context["form"] = form

        data = {
            'form': ProductForm(request.POST or None, request.FILES or None, instance=obj),
        }

        return render(request, "store/dashboard.html", data)
    else:
        print('not authenticated')
        return redirect('/')


# delete view for details
def delete_view(request, id):
    if request.user.is_superuser:
        # dictionary for initial data with
        # field names as keys

        # fetch the object related to passed id
        obj = get_object_or_404(Product, id=id)

        if request.method == "POST":
            # delete object
            obj.delete()
            # after deleting redirect to
            # home page
            return HttpResponseRedirect("/dashboard?ecom=2")

        data = {
            'data': Product.objects.get(id=id),
        }

        return render(request, "store/dashboard.html", data)
    else:
        print('not authenticated')
        return redirect('/')
