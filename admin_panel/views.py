from django.shortcuts import render
from django.views.generic import TemplateView, ListView, View
from .mixins import AdminRequiredMixin
from shop.models import Review
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.html import format_html


class AdminPanel(AdminRequiredMixin, TemplateView):
    template_name = 'admin_stuff/admin_panel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unmodered_reviews_count'] = Review.objects.filter(is_moderated=False).count()
        return context


class ReviewModerationView(AdminPanel, ListView):
    template_name = 'admin_stuff/review_moderation.html'
    paginate_by = 5
    object_list = Review.objects.filter(is_moderated=False).order_by('-created_at')


class AcceptReviewView(AdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        review = Review.objects.get(id=self.kwargs['review_id'])
        review.is_moderated = True
        review.save()
        messages.success(request, format_html("<strong class='font-bold'>Успішно!</strong> Відгук для \"{}\" було схвалено", review.on_product.name))
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


class DeclineReviewView(AdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        review = Review.objects.get(id=self.kwargs['review_id'])
        review.delete()
        messages.error(request, format_html("<strong class='font-bold'>Успішно!</strong> Відгук для \"{}\" було видалено.", review.on_product.name))
        return HttpResponseRedirect(request.META["HTTP_REFERER"])