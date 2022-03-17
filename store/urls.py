from django.urls import path, include
from django.shortcuts import render, redirect

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('shop', views.store_View, name='Shop'),
    path('store', views.store_View, name='Store'),
    path('cart/', views.cart_View, name='Cart'),
    path('checkout/', views.checkout_View, name='Checkout'),

    path('login-shop', views.login_View, name="Login-Shop"),
    path('logout', views.logoutView, name="Logout"),
    path('404', views.handler404, name="404"),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
