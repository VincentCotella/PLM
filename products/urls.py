from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'products'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),  # Tableau de bord
    path('products/', views.product_list, name='product_list'),  # Liste des produits
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),  # Détail du produit
    path('add/', views.add_product, name='add_product'),  # Formulaire pour ajouter un produit
    path('generate_report/', views.generate_report, name='generate_report'),  # Ajoutez cette ligne
    path('products/<int:product_id>/stl/', views.view_stl, name='view_stl'),
    path('stl-proxy/<str:file_id>/', views.proxy_stl, name='proxy_stl'),
    # Routes pour la Simulation de Coût
    path('cost-simulations/', views.cost_simulation_list, name='cost_simulation_list'),
    path('cost-simulations/create/', views.cost_simulation_create, name='cost_simulation_create'),
    path('cost-simulations/<int:simulation_id>/', views.cost_simulation_detail, name='cost_simulation_detail'),
]
