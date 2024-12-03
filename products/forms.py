from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['reference', 'name', 'product_range', 'is_modified', 'created_by', 'stl_file']
        widgets = {
            'stl_file': forms.URLInput(attrs={'placeholder': 'Enter STL file URL'})
        }