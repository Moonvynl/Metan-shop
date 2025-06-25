from django import template
from ..models import Review

register = template.Library()

@register.filter
def calculate_discount_price(price, discount):
    discounted_price = price - (price * discount / 100)
    return "{:.2f}".format(discounted_price)

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.simple_tag
def total_price_with_discount(price, discount, quantity):
    try:
        discounted_price = price - (price * discount / 100)
        return "{:.2f}".format(discounted_price * quantity)
    except (ValueError, TypeError):
        return "0.00"

@register.filter
def stars_for_review_moderation(rating):
    return "★" * rating

@register.filter
def product_reviews_count(product_id):
    return Review.objects.filter(on_product_id=product_id).filter(is_moderated=True).count()