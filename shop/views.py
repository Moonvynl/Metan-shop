from django.shortcuts import render
from django.views.generic import TemplateView,View,ListView
from .models import *
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import ReviewCreateForm
from django.views.generic.edit import CreateView
from django.utils.html import format_html
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid


def get_anon_id(request):
    session_key = request.session.get('anon_user_session_key')
    if not session_key:
        session_key = str(uuid.uuid4())
        request.session['anon_user_session_key'] = session_key
        request.session.modified = True
    return session_key

def get_or_create_cart(request):
    if request.user.is_authenticated:
        user = request.user
        if not Cart.objects.filter(user=user).exists():
            Cart.objects.create(user=user)
        else:
            cart = Cart.objects.get(user=user)
    else:
        user = get_anon_id(request)
        if not Cart.objects.filter(session_key=user).exists():
            Cart.objects.create(session_key=user)
        else:
            cart = Cart.objects.filter(session_key=user).first()
    return cart

class BaseView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        if self.request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=self.request.user)[0]
            cart_products_count = cart.total_products_count
        else:
            session_key = get_anon_id(self.request)
            anon_cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()
            if anon_cart:
                cart_products_count = anon_cart.total_products_count
            else:
                Cart.objects.create(session_key=session_key, user=None)
                cart_products_count = 0
        context['cart_products_count'] = cart_products_count
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
        cart = get_or_create_cart(self.request)

        total_price = 0
        for product in cart.productforcart_set.all():
            total_price += product.product.price * product.quantity
        context['products'] = cart.productforcart_set.all()
        context['total_price'] = total_price
        return context


class CreateReviewView(BaseView, CreateView, LoginRequiredMixin):
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

    cart = get_or_create_cart(request)

    if request.GET.get('quantity'):
        quantity = request.GET.get('quantity')
    else:
        quantity = 1

    product_for_cart = ProductForCart.objects.filter(cart=cart, product=product).first()
    if not product_for_cart:
        product_for_cart = ProductForCart(cart=cart, product=product)

    if cart.productforcart_set.filter(id=product_for_cart.id, cart=cart).exists():
        product_for_cart.quantity += int(quantity) if quantity else 1
        product_for_cart.save()
        messages.success(request, format_html("<strong class='font-bold'>Успішно!</strong> \"{}\" додано до кошика.", product.name))
    else:
        product_for_cart.quantity = int(quantity)
        product_for_cart.save()
        cart.productforcart_set.add(product_for_cart)
        messages.success(request, format_html("<strong class='font-bold'>Успішно!</strong> \"{}\" додано до кошика.", product.name))
    return HttpResponseRedirect(request.META["HTTP_REFERER"])