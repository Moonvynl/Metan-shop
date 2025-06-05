from django import template

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
