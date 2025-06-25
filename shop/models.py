from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


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
    under_category = models.ForeignKey(UnderCategory, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    reviews = models.ForeignKey('Review', on_delete=models.CASCADE, null=True, blank=True)

    def calculate_discounted_price(self):
        if self.discount:
            return self.price * (1 - self.discount / 100)
        return self.price
    
    def __str__(self):
        return self.name
    
    def calculate_rating(self):
        reviews = self.product_reviews.filter(is_moderated=True).all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            total_rating = total_rating / len(reviews)
            if total_rating.is_integer():
                return int(total_rating)
            elif total_rating == 0:
                return 0
            else:
                return round(total_rating, 1)


class Review(models.Model):
    on_product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_moderated = models.BooleanField(default=False)

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return f"Review by {self.author.username} on {self.on_product.name}"


class ProductForCart(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return f"{self.product.name} for {self.cart}"


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True, unique=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(user__isnull=False, session_key__isnull=True) |
                    models.Q(user__isnull=True, session_key__isnull=False),
                name='user_or_session_key_present' 
            )
        ]
        unique_together = ('user',)


    def __str__(self):
        return f"Cart for {self.user.username}"
    
    @property
    def total_products_count(self):
        counter = 0
        for product in self.productforcart_set.all():
            counter += product.quantity
        return counter

