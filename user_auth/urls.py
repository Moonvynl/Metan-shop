from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

urlpatterns = [
    path('login/', LoginView.as_view(template_name='user_auth/login.html' , extra_context={'next': reverse_lazy('shop:base')}), name='login'),
    path('register/', RegisterView.as_view(template_name='user_auth/register.html'), name='register'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('shop:home_page')), name='logout'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/info/', ProfileInfo.as_view(), name='profile_info'),
]

app_name = 'user_auth'