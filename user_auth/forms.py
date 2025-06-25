from typing import Any
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserInformation
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["avatar","username", "password1", "password2"]


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        fields = ["email", "phone_number", "shipping_type", "first_name", "last_name"]