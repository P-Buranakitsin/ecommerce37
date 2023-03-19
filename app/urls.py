from django.urls import path, include
from app import views
from django.contrib import admin

app_name = 'app'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('commodity/<int:c_id>/', views.CommodityView.as_view(), name='commodity'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('contactUs/', views.ContactUsView.as_view(), name='contactUs'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('add_to_cart/', views.AddtoCartView.as_view(), name='add_to_cart'),
    path('remove_from_cart/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('update_cart/', views.UpdateCartView.as_view(), name='update_cart'),
    path('checkout_cart/', views.CheckoutCartView.as_view(), name='checkout_cart'),
]

