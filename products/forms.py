from django import forms
from .models import Product, Site

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['reference', 'name', 'product_range', 'site', 'is_modified', 'created_by', 'stl_file']
        widgets = {
            'stl_file': forms.URLInput(attrs={'placeholder': 'Enter STL file URL'}),
            'site': forms.Select(attrs={'class': 'form-select mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'})
        }