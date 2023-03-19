from django.contrib import admin
from app.models import UserProfile, Commodities, CartItem

class CommoditiesAdmin(admin.ModelAdmin):
    readonly_fields = ('c_id',)

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Commodities, CommoditiesAdmin)
admin.site.register(CartItem)
