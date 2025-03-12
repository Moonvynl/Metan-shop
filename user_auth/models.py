from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='/default_avatar.png')

    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    shopping_cart = models.ManyToManyField('shop.Product', related_name='users_in_cart', blank=True)
    def __str__(self):
        return self.username