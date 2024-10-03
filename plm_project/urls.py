from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),  # Inclure les URLs de l'application products
    path('accounts/', include('django.contrib.auth.urls')),  # Inclure les URLs d'authentification intégrées
]
