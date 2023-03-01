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


class Order(models.Model):
    id = models.AutoField(primary_key=True, max_length=20)
    product_name = models.CharField(verbose_name='商品名',max_length=200, blank=True)
    num = models.IntegerField(verbose_name='购买数量')
    price = models.DecimalField(verbose_name='价格', max_digits=10, decimal_places=2, default=0)  #长度为8，精度为2
    address = models.CharField(verbose_name='地址',max_length=2000)
    phone = models.CharField(verbose_name='手机号',max_length=11)
    name = models.CharField(verbose_name='姓名',max_length=20)
    message = models.CharField(verbose_name='留言',max_length=20)


class Comment(models.Model):
    id = models.AutoField(primary_key=True, max_length=20)
    order_id = models.IntegerField(verbose_name='商品id')
    content = models.CharField(verbose_name='商品内容',max_length=2000)
