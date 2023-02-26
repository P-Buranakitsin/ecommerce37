from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    
class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=20)
    username = models.CharField(max_length=200, blank=True)
    user_email = models.EmailField(unique=True)

    def __str__(self):
        return self.user_id

class Commodities(models.Model):
    c_id = models.CharField(primary_key=True, max_length=20)
    c_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='commodities/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    #type
    #inventory

    def __str__(self):
        return self.c_id

class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commodities = models.ForeignKey(Commodities, on_delete=models.CASCADE)
    amount = models.ImageField(default=1)
