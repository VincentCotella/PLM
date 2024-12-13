# products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import logout
from django.views import View
from django.db.models import Sum
from django.views.decorators.http import require_http_methods
import json
from django.core.serializers.json import DjangoJSONEncoder
import requests
from django.conf import settings

from .models import Product, Site, Project, CostSimulation, Equipment, Inventory, Sale, ChangeLog
from .forms import ProductForm, CostSimulationForm, SiteForm, EquipmentForm, InventoryForm, SaleForm

@login_required
def dashboard(request):
    products = Product.objects.all()
    sites = Site.objects.all()
    
    # Remplacer modification_history par logs
    logs = ChangeLog.objects.select_related('content_type', 'user').order_by('-date_modified')[:5]

    total_stock = Inventory.objects.aggregate(total=Sum('quantity'))['total'] or 0
    total_sales = Sale.objects.aggregate(total=Sum('quantity'))['total'] or 0
    low_stock_products = Inventory.objects.select_related('product').order_by('quantity')[:5]
    top_selling = Sale.objects.values('product__name').annotate(total_sold=Sum('quantity')).order_by('-total_sold')[:5]
    simulations = CostSimulation.objects.select_related('product').all()

    # Données pour le graphique des catégories de produits
    agrifood_products_data = list(products.filter(product_range__category='AG').values('id', 'name'))
    perfumery_products_data = list(products.filter(product_range__category='PE').values('id', 'name'))

    context = {
        'products_count': products.count(),
        'sites_count': sites.count(),
        'total_stock': total_stock,
        'total_sales': total_sales,
        'low_stock_products': low_stock_products,
        'top_selling': top_selling,
        'sites': sites,
        'simulations': simulations,
        'logs': logs,
        'agrifood_products_data': json.dumps(agrifood_products_data, cls=DjangoJSONEncoder),
        'perfumery_products_data': json.dumps(perfumery_products_data, cls=DjangoJSONEncoder),
    }
    return render(request, 'products/dashboard.html', context)

@login_required
def generate_report(request):
    return HttpResponse("Ceci est un exemple de rapport pour la production.")

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:product_list')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})

class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('/')

    def get(self, request):
        logout(request)
        return redirect('/')

@login_required
def view_stl(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product, 'debug': settings.DEBUG}
    return render(request, 'products/stl_viewer.html', context)

@require_http_methods(["GET"])
def proxy_stl(request, file_id):
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return HttpResponse(
            response.content,
            content_type='application/octet-stream',
            headers={
                'Content-Disposition': 'attachment; filename="model.stl"',
                'Access-Control-Allow-Origin': '*',
            }
        )
    except Exception as e:
        return HttpResponse(f"Erreur lors de la récupération du fichier STL: {str(e)}", status=500)

@login_required
def cost_simulation_list(request):
    simulations = CostSimulation.objects.select_related('product').all()
    return render(request, 'products/cost_simulation_list.html', {'simulations': simulations})

@login_required
def cost_simulation_create(request):
    if request.method == 'POST':
        form = CostSimulationForm(request.POST)
        if form.is_valid():
            simulation = form.save()
            return redirect('products:cost_simulation_detail', simulation_id=simulation.id)
    else:
        form = CostSimulationForm()
    return render(request, 'products/cost_simulation_form.html', {'form': form})

@login_required
def cost_simulation_detail(request, simulation_id):
    simulation = get_object_or_404(CostSimulation, id=simulation_id)
    return render(request, 'products/cost_simulation_detail.html', {'simulation': simulation})

@login_required
def production_site_list(request):
    sites = Site.objects.all()
    return render(request, 'products/production_site_list.html', {'sites': sites})

@login_required
def production_site_create(request):
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:production_site_list')
    else:
        form = SiteForm()
    return render(request, 'products/production_site_form.html', {'form': form})

@login_required
def production_site_detail(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    return render(request, 'products/production_site_detail.html', {'site': site})

@login_required
def production_site_edit(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    if request.method == 'POST':
        form = SiteForm(request.POST, instance=site)
        if form.is_valid():
            form.save()
            return redirect('products:production_site_detail', site_id=site.id)
    else:
        form = SiteForm(instance=site)
    return render(request, 'products/production_site_form.html', {'form': form, 'site': site})

@login_required
def production_site_delete(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    if request.method == 'POST':
        site.delete()
        return redirect('products:production_site_list')
    return render(request, 'products/production_site_confirm_delete.html', {'site': site})

@login_required
def equipment_list(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    equipment = site.equipment.all()
    return render(request, 'products/equipment_list.html', {'site': site, 'equipment': equipment})

@login_required
def equipment_create(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save()
            return redirect('products:equipment_list', site_id=site.id)
    else:
        form = EquipmentForm(initial={'site': site})
    return render(request, 'products/equipment_form.html', {'form': form, 'site': site})

@login_required
def equipment_edit(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('products:equipment_list', site_id=equipment.site.id)
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'products/equipment_form.html', {'form': form, 'site': equipment.site, 'equipment': equipment})

@login_required
def equipment_delete(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    site = equipment.site
    if request.method == 'POST':
        equipment.delete()
        return redirect('products:equipment_list', site_id=site.id)
    return render(request, 'products/equipment_confirm_delete.html', {'equipment': equipment, 'site': site})


@login_required
def inventory_list(request):
    inventories = Inventory.objects.select_related('product').all()
    return render(request, 'products/inventory_list.html', {'inventories': inventories})

@login_required
def inventory_create(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:inventory_list')
    else:
        form = InventoryForm()
    return render(request, 'products/inventory_form.html', {'form': form, 'title': "Ajouter un Inventaire"})

@login_required
def inventory_edit(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            return redirect('products:inventory_list')
    else:
        form = InventoryForm(instance=inventory)
    return render(request, 'products/inventory_form.html', {'form': form, 'title': "Modifier l'Inventaire"})

@login_required
def sale_list(request):
    sales = Sale.objects.select_related('product', 'salesperson').all()
    return render(request, 'products/sale_list.html', {'sales': sales})

@login_required
def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            # Vous pouvez assigner le current user comme salesperson si nécessaire :
            # sale.salesperson = request.user
            sale.save()
            return redirect('products:sale_list')
    else:
        form = SaleForm()
    return render(request, 'products/sale_form.html', {'form': form, 'title': "Ajouter une Vente"})

@login_required
def sale_edit(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect('products:sale_list')
    else:
        form = SaleForm(instance=sale)
    return render(request, 'products/sale_form.html', {'form': form, 'title': "Modifier la Vente"})