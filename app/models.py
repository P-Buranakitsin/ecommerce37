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