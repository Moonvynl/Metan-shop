from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(UnderCategory)
admin.site.register(ProductForCart)
admin.site.register(Cart)