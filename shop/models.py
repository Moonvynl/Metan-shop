from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UnderCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='undercategory')

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    under_category = models.ForeignKey(UnderCategory, on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    reviews = models.ForeignKey('Review', on_delete=models.CASCADE, null=True, blank=True)


class Review(models.Model):
    on_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)