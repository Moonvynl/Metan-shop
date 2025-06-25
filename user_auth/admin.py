from django.contrib import admin
from .models import CustomUser, UserInformation

admin.site.register(CustomUser)
admin.site.register(UserInformation)