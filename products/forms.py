from django import forms
from .models import Product, Site, CostSimulation

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['reference', 'name', 'product_range', 'site', 'is_modified', 'created_by', 'stl_file']
        widgets = {
            'stl_file': forms.URLInput(attrs={'placeholder': 'Enter STL file URL'}),
            'site': forms.Select(attrs={'class': 'form-select mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'})
        }

class CostSimulationForm(forms.ModelForm):
    class Meta:
        model = CostSimulation
        fields = [
            'product',
            'raw_material_cost',
            'labor_cost',
            'overhead_cost',
            'margin',
        ]
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'raw_material_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'labor_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'overhead_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'margin': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'product': 'Produit',
            'raw_material_cost': 'Coût des Matières Premières (€)',
            'labor_cost': 'Coût de la Main-d\'Œuvre (€)',
            'overhead_cost': 'Frais Généraux (€)',
            'margin': 'Marge Bénéficiaire (%)',
        }
