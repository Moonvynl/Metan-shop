from django.shortcuts import render
from django.views.generic import TemplateView,View,ListView
from .models import *
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import ReviewCreateForm
from django.views.generic.edit import CreateView
from django.utils.html import format_html
from .mixins import *


class BaseView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        cart = Cart.objects.filter(user=self.request.user).first() if self.request.user.is_authenticated else None
        quantity_cart_sum = 0
        if cart:
            for product in ProductForCart.objects.filter(user = self.request.user):
                quantity_cart_sum += product.quantity
        context['cart_products_count'] = quantity_cart_sum
        return context


class HomePageView(BaseView):
    template_name = 'shop/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all().order_by('-is_available')
        return context


class ProductDetailView(BaseView):
    template_name = 'shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['product'] = Product.objects.get(pk=self.kwargs['product_id'])
        context['reviews'] = Review.objects.filter(on_product=context['product']).filter(is_moderated=True)[:5]
        context['interestings'] = Product.objects.order_by('-pk').filter(category=context['product'].category)[:4]
        context['total_reviews'] = Review.objects.filter(on_product=context['product']).filter(is_moderated=True).count()
        return context


class CartView(BaseView):
    template_name = 'shop/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = ProductForCart.objects.filter(user=self.request.user).order_by('-created_at')
        total_price = 0
        for product in products:
            total_price += product.product.price * product.quantity
        context['products'] = products
        print(products)
        context['total_price'] = total_price
        return context

class CreateReviewView(BaseView, CreateView):
    def post(self, request, *args, **kwargs):
        form = ReviewCreateForm(data=request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.on_product = Product.objects.get(pk=self.kwargs['product_id'])
            review.save()
            messages.success(request, format_html("<strong class='font-bold'>Успішно!</strong> Ваш відгук буде додано після проходження модерації."))
        else:
            messages.error(request, "Будь ласка, виправте помилки у формі.")
            print(form.errors)
        return redirect('shop:product_detail', product_id=self.kwargs['product_id'])


def add_quantity(request, product_id):
    product = ProductForCart.objects.get(id=product_id)
    product.quantity += 1
    product.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

def remove_quantity(request, product_id):
    product = ProductForCart.objects.get(id=product_id)
    if product.quantity > 1:
        product.quantity -= 1
        product.save()
    else:
        product.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

def delete_product_for_cart(request, product_id):
    product = ProductForCart.objects.get(id=product_id)
    product.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user).first()

        if request.GET.get('quantity'):
            quantity = request.GET.get('quantity')
        else:
            quantity = 1
        
        if not cart:
            cart = Cart.objects.create(user=user)

        product_for_cart = ProductForCart.objects.filter(user=user, product=product).first()
        if not product_for_cart:
            product_for_cart = ProductForCart.objects.create(user=user, product=product)
            
        if cart.products.filter(id=product_for_cart.id, user=user).exists():
            product_for_cart.quantity += int(quantity) if quantity else 1
            product_for_cart.save()
            messages.success(request, format_html("<strong class='font-bold'>Успішно!</strong> \"{}\" додано до кошика.", product.name))
        else:
            product_for_cart.quantity = int(quantity)
            product_for_cart.save()
            cart.products.add(product_for_cart)
            messages.success(request, format_html("<strong class='font-bold'>Успішно!</strong> \"{}\" додано до кошика.", product.name))
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        return redirect('user_auth:login')


class AdminPanel(AdminRequiredMixin, TemplateView):
    template_name = 'admin_stuff/admin_panel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unmodered_reviews_count'] = Review.objects.filter(is_moderated=False).count()
        return context


class ReviewModerationView(AdminRequiredMixin, TemplateView, ListView):
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