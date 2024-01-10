from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('signup', views.signup),
    path('', views.login),
    path('theme', views.theme, name="theme"),
    path('contact', views.contact)
]