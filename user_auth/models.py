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

    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    access = models.CharField(max_length=10, choices=ACCESS_CHOICES, default='user')

    def __str__(self):
        return self.username