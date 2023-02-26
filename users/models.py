from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.

class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=20)
    username = models.CharField(max_length=200, blank=True)
    user_email = models.EmailField(unique=True)

    def __str__(self):
        return self.user_id