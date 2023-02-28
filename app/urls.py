from django.urls import path, include
from app import views
from app import order
from app import comment
from django.contrib import admin

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('buy/', views.buy , name='buy'),


    path('order/pay', order.pay, name='pay'),
    path('comment/', comment.commit, name='commit'),
]

