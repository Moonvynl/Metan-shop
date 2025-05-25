from django.urls import path
from django.urls import reverse_lazy
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:product_id>/add_to_cart/', add_to_cart, name='add_to_cart'),
]
app_name = 'shop'