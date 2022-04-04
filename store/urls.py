from django.urls import path, include
from django.shortcuts import render, redirect

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.store_View, name='Shop'),
    path('shop', views.store_View, name='Shop'),
    path('store', views.store_View, name='Store'),
    path('cart/', views.cart_View, name='Cart'),
    path('checkout/', views.checkout_View, name='Checkout'),
    path('contact', views.contactView, name='Contact'),

    path('dashboard', views.dashboard_View, name='Dashboard'),

    path('update_item/', views.updateItem, name='update_item'),

    path('process_order/', views.processOrder, name="process_order"),

    path('login-shop', views.login_View, name="Login-Shop"),
    path('register-shop', views.register_View, name="Register"),
    path('logout', views.logoutView, name="Logout"),
    path('404', views.handler404, name="404"),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
