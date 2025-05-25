from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from .forms import RegisterForm
from django.shortcuts import redirect
import random

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
