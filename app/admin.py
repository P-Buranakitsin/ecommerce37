from django.contrib import admin
from app.models import UserProfile, Commodities, CartItem

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Commodities)
admin.site.register(CartItem)
