from django.urls import path
from django.urls import reverse_lazy
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:product_id>/add_to_cart/', add_to_cart, name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add_quantity/<int:product_id>/', add_quantity, name='add_quantity'),
    path('cart/remove_quantity/<int:product_id>/', remove_quantity, name='remove_quantity'),
    path('cart/delete_product_for_cart/<int:product_id>/', delete_product_for_cart, name='delete_product_for_cart'),
    path('product/<int:product_id>/create_review/', CreateReviewView.as_view(), name='create_review'),

    path('admin_panel/', AdminPanel.as_view(), name='admin_panel'),
    path('admin_panel/review_moderation/', ReviewModerationView.as_view(), name='review_moderation'),
    path('admin_panel/review_moderation/accept_review/<int:review_id>/', AcceptReviewView.as_view(), name='accept_review'),
    path('admin_panel/review_moderation/decline_review/<int:review_id>/', DeclineReviewView.as_view(), name='decline_review'),

]
app_name = 'shop'