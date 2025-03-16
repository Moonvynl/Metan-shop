from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib import messages

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
        context['product'] = Product.objects.get(pk=self.kwargs['pk'])
        context['reviews'] = Review.objects.filter(on_product=context['product'])
        context['interestings'] = Product.objects.order_by('-pk').filter(category=context['product'].category)[:4]
        return context


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            cart = Cart.objects.create(user=user)

        product_for_cart = ProductForCart.objects.filter(user=user, product=product).first()
        if not product_for_cart:
            product_for_cart = ProductForCart.objects.create(user=user, product=product)
            
        if cart.products.filter(id=product_for_cart.id, user=user).exists():
            product_for_cart.quantity += 1
            product_for_cart.save()
            messages.success(request, f"{product.name} sucsessfully added to cart")
        else:
            cart.products.add(product_for_cart)
            messages.success(request, f"{product.name} sucsessfully added to cart")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        return redirect('user_auth:login')
