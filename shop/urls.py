from django.urls import path
from django.urls import reverse_lazy
from .views import *

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
]

app_name = 'shop'