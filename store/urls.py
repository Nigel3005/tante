from django.urls import path, include
from django.shortcuts import render, redirect

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.store_View, name='Shop'),
    path('shop', views.store_View, name='Shop'),
    path('view/<int:id>', views.product_View, name='Shop'),
    path('store', views.store_View, name='Store'),
    path('cart/', views.cart_View, name='Cart'),
    path('checkout/', views.checkout_View, name='Checkout'),
    path('contact', views.contactView, name='Contact'),

    path('dashboard', views.dashboard_View, name='Dashboard'),

    path('update_item/', views.updateItem, name='update_item'),

    path('process_order/', views.processOrder, name="process_order"),

    # CRUD
    path('dashboard/create', views.create_view, name='Create'),
    path('list', views.list_view, name='List'),
    path('dashboard/<int:id>', views.detail_view, name='Detail'),
    path('dashboard/<int:id>/update', views.update_view, name='Update'),
    path('dashboard/<int:id>/delete', views.delete_view, name='Delete'),

    path('login-shop', views.login_View, name="Login-Shop"),
    path('register-shop', views.register_View, name="Register"),
    path('logout', views.logoutView, name="Logout"),
    path('404', views.handler404, name="404"),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
