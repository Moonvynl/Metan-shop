from django import template

register = template.Library()

@register.filter
def calculate_discount_price(price, discount):
    discounted_price = price - (price * discount / 100)
    return "{:.2f}".format(discounted_price)
