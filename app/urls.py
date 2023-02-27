from django.urls import path, include
from app import views
from django.contrib import admin

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),

    path('cart/', views.viewShoppingCart, name='ShoppingCart')
]

