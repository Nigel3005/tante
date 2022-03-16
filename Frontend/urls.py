from django.urls import path, include
from django.shortcuts import render, redirect

from . import views
from .views import detail_view, delete_view

urlpatterns = [
    path('', views.indexView, name='Home'),
    path('home', views.indexView, name='Home'),

    path('contact', views.contactView, name='Contact'),

    path('create', views.create_view, name='Create'),
    path('list', views.list_view, name='List'),
    path('<int:id>', detail_view, name='Detail'),
    path('<int:id>/update', views.update_view, name='Update'),
    path('<int:id>/delete', delete_view, name='Delete'),

    path('login', views.loginView, name="Login"),
    path('logout', views.logoutView, name="Logout"),
    path('404', views.handler404, name="404"),

]

