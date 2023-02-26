from django.urls import path, include
from app import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('login/', views.login, name='login'),

    path('users/', include('users.urls'))

]

