from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['reference', 'name', 'product_range', 'is_modified', 'created_by']  # Les champs que vous voulez afficher