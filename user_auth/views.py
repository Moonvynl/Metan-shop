from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from .forms import RegisterForm
from django.shortcuts import redirect
import random
from shop.views import BaseView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserInfoForm
from .models import UserInformation
from django.contrib import messages

avatars = [
    "\default_avatar1.png",
    "\default_avatar2.png",
    "\default_avatar3.png",
    "\default_avatar4.png",
    "\default_avatar5.png",
    "\default_avatar6.png",
    "\default_avatar7.png",

]

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "user_auth/register.html"
    success_url = reverse_lazy("shop:home_page")
    def form_valid(self, form):
        user = form.save()
        user.avatar = random.choice(avatars)
        user.save()
    
        if user:
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            if user.is_authenticated:
                return HttpResponseRedirect(self.success_url)
            else:
                return redirect("user_auth:login")

        return super().form_valid(form)


class ProfileView(BaseView, LoginRequiredMixin):
    template_name = 'user_auth/user_profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ProfileInfo(ProfileView, LoginRequiredMixin):
    template_name = 'user_auth/user_profile/profile_info.html'

    def post(self, request, *args, **kwargs):
        if UserInformation.objects.filter(user=request.user).exists():
            userinfo = UserInformation.objects.get(user=request.user)
            form = UserInfoForm(data=request.POST, instance=userinfo)
        else:
            form = UserInfoForm(data=request.POST)

        if form.is_valid():
            info = form.save(commit=False)
            info.user = request.user
            info.save()
            messages.success(request, "Інформацію оновлено.")
            return redirect('user_auth:profile_info')
        else:
            messages.error(request, "Помилка.")
            print(form.errors)
            return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_shipping = UserInformation.objects.get_or_create(user=self.request.user)[0].shipping_type
        shipping_choices = UserInformation.SHIPPING_CHOICES
        if current_shipping is not None:
            shipping_choices = [choice for choice in shipping_choices if choice[0] == current_shipping] + [choice for choice in shipping_choices if choice[0] != current_shipping]
        context['shipping_choices'] = shipping_choices
        context['form'] = UserInfoForm(instance=UserInformation.objects.get_or_create(user=self.request.user)[0])
        return context