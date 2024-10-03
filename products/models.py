from django.db import models
from django.contrib.auth.models import User

class ProductRange(models.Model):
    CATEGORY_CHOICES = [
        ('AG', 'Agrifood'),
        ('PE', 'Perfumery'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.get_category_display()} - {self.name}"

class Product(models.Model):
    reference = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    product_range = models.ForeignKey(ProductRange, on_delete=models.CASCADE)
    is_modified = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.reference:
            prefix = 'AG_' if self.product_range.category == 'AG' else 'PE_'
            self.reference = f"{prefix}00{'M' if self.is_modified else 'S'}000"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} - {self.name}"

class BOM(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    requirements = models.TextField()
    manufacturing_process = models.TextField()
    resources = models.TextField()
