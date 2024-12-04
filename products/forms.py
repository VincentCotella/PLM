from django import forms
from .models import Product, Site, CostSimulation, Site, Equipment

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


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['name', 'location', 'capacity', 'is_active', 'latitude', 'longitude']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'location': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'mt-1'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'step': 'any'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'step': 'any'
            }),
        }

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['site', 'name', 'equipment_type', 'maintenance_due', 'status']
        widgets = {
            'site': forms.Select(attrs={
                'class': 'form-select mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'equipment_type': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'maintenance_due': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
            }),
        }
        labels = {
            'site': 'Site de Production',
            'name': 'Nom de l\'Équipement',
            'equipment_type': 'Type d\'Équipement',
            'maintenance_due': 'Date de Maintenance',
            'status': 'Statut',
        }