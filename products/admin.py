from django.contrib import admin
from .models import Product, ProductRange, BOM

# Enregistrer les modèles dans l'interface d'administration
admin.site.register(Product)
admin.site.register(ProductRange)
admin.site.register(BOM)
