from django.contrib import admin
from app.models import UserProfile, Commodities, CartItem, Purchase

class CommoditiesAdmin(admin.ModelAdmin):
    readonly_fields = ('c_id',)

class PurchaseAdmin(admin.ModelAdmin):
    readonly_fields = ('purchase_date',)

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Commodities, CommoditiesAdmin)
admin.site.register(CartItem)
admin.site.register(Purchase, PurchaseAdmin)