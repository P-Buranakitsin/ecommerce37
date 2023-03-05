from django.urls import path, include
from app import views
from django.contrib import admin

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('commodity/<slug:c_id>/', views.CommodityView.as_view(), name='commodity'),
    path('cart/', views.viewShoppingCart, name='ShoppingCart'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]

