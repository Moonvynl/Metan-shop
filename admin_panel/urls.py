from django.urls import path
from django.urls import reverse_lazy
from .views import *

urlpatterns = [ 
    path('admin_panel/', AdminPanel.as_view(), name='admin_panel'),
    path('admin_panel/review_moderation/', ReviewModerationView.as_view(), name='review_moderation'),
    path('admin_panel/review_moderation/accept_review/<int:review_id>/', AcceptReviewView.as_view(), name='accept_review'),
    path('admin_panel/review_moderation/decline_review/<int:review_id>/', DeclineReviewView.as_view(), name='decline_review'),
]

app_name = 'admin_panel'