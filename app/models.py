from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='images/profile_images', blank=True)

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
    
    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return ''

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commodities = models.ForeignKey(Commodities, on_delete=models.PROTECT)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + "_" + self.commodities.c_name + "_" + str(self.commodities.c_id)
    
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
