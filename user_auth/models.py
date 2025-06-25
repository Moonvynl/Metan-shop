from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ACCESS_CHOICES = [
        ('user', 'User'),
        ('CM', 'ContentManager'),
        ('OM', 'OrderManager'),
        ('AD', 'Admin'),
    ]

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='/default_avatar.png')
    access = models.CharField(max_length=10, choices=ACCESS_CHOICES, default='user')

    def __str__(self):
        return self.username


class UserInformation(models.Model):
    SHIPPING_CHOICES = [
        ('up', 'УкрПошта'),
        ('np', 'Нова Пошта'),
        ('me', 'Meest Express'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    shipping_type = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s information"