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
    # Routes pour les sites de production
    path('production-sites/', views.production_site_list, name='production_site_list'),
    path('production-sites/create/', views.production_site_create, name='production_site_create'),
    path('production-sites/<int:site_id>/', views.production_site_detail, name='production_site_detail'),
    path('production-sites/<int:site_id>/edit/', views.production_site_edit, name='production_site_edit'),
    path('production-sites/<int:site_id>/delete/', views.production_site_delete, name='production_site_delete'),
   
]
