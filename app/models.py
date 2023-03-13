from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
class Type(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return self.name

class Commodities(models.Model):
    #c_id = models.CharField(primary_key=True, max_length=20)
    c_id = models.BigAutoField(primary_key=True)
    c_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='Commodities/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    #inventory
    class Meta:
        verbose_name_plural = 'commodities'

    def __str__(self):
        return self.c_name

class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commodities = models.ForeignKey(Commodities, on_delete=models.PROTECT)
    amount = models.IntegerField()
    """
    def __init__(self, *args, **kwargs):
        self.items = []
        self.total_price = 0

    def add_commodities(self, commodities):
        self.price += commodities.price
        for item in self.items:
            if item.commodities.c_id == commodities.c_id:
                item.amount += 1
                return
        self.items.append()
    """
