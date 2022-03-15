from django.urls import path, include
from django.shortcuts import render, redirect

from . import views

urlpatterns = [
    path('', views.indexView, name='Home'),
    path('home', views.indexView, name='Home'),
    path('contact', views.contactView, name='Contact'),
    path('create', views.create_view_page, name='Create'),
    path('login', views.loginView, name="Login"),
    path('logout', views.logoutView, name="Logout"),
    path('404', views.handler404, name="404"),

]

