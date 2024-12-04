# your_app/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Product, ProductRange, Site, Project, ModificationHistory, CostSimulation, Equipment
from .forms import ProductForm, CostSimulationForm, SiteForm, EquipmentForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
import requests
from django.views.decorators.http import require_http_methods

@login_required
def dashboard(request):
    products = Product.objects.all()
    ranges = ProductRange.objects.all()
    sites = Site.objects.all()
    projects = Project.objects.all()
    modification_history = ModificationHistory.objects.all()
    simulations = CostSimulation.objects.select_related('product').order_by('-created_at')[:10]  

    # Serialize QuerySets into lists of dictionaries
    agrifood_products_data = list(
        products.filter(product_range__category='AG').values('id', 'name')
    )
    perfumery_products_data = list(
        products.filter(product_range__category='PE').values('id', 'name')
    )

    cost_simulations_data = []
    for simulation in simulations:
        cost_simulations_data.append({
            'product_name': simulation.product.name,
            'calculated_price': float(simulation.calculated_price),
            'margin': float(simulation.margin),
            'created_at': simulation.created_at.strftime('%Y-%m-%d %H:%M'),
        })

    # Préparer les données des sites pour le JavaScript
    sites_data = [
        {
            'name': site.name,
            'lat': float(site.latitude) if site.latitude else None,
            'lon': float(site.longitude) if site.longitude else None,
            'location': site.get_location_display(),
            'capacity': site.capacity
        }
        for site in sites
        if site.latitude and site.longitude
    ]
    sites_json = json.dumps(sites_data, cls=DjangoJSONEncoder)

    context = {
        'products': products,
        'ranges': ranges,
        'sites': sites,
        'projects': projects,
        'agrifood_products_data': json.dumps(agrifood_products_data, cls=DjangoJSONEncoder),
        'perfumery_products_data': json.dumps(perfumery_products_data, cls=DjangoJSONEncoder),
        'cost_simulations_data': json.dumps(cost_simulations_data, cls=DjangoJSONEncoder),
        'modification_history': modification_history,
        'simulations': simulations,  # Ajouter les simulations au contexte
        'sites_json': sites_json,    # Ajouter les données des sites en JSON
    }
    return render(request, 'products/dashboard.html', context)

@login_required
def generate_report(request):
    # Ajoutez ici la logique de génération du rapport.
    return HttpResponse("This is a sample report for production.")

@login_required
def product_list(request):
    products = Product.objects.all()  # Récupérer tous les objets Product
    context = {
        'products': products,
    }
    return render(request, 'products/product_list.html', context)

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
            return redirect('products:product_list')  # Redirige vers la liste des produits après ajout
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})

from django.contrib.auth.views import LogoutView

class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('/')  # Redirect to homepage after logout

    def get(self, request):
        logout(request)  # Ensure the user is logged out on GET requests
        return redirect('/')  # Redirect to homepage after logout

@login_required
def view_stl(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
        'debug': settings.DEBUG
    }
    return render(request, 'products/stl_viewer.html', context)

@require_http_methods(["GET"])
def proxy_stl(request, file_id):
    # Google Drive direct download URL
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        # Return the file content with appropriate headers
        return HttpResponse(
            response.content,
            content_type='application/octet-stream',
            headers={
                'Content-Disposition': 'attachment; filename="model.stl"',
                'Access-Control-Allow-Origin': '*',
            }
        )
    except Exception as e:
        return HttpResponse(
            f"Error fetching STL file: {str(e)}",
            status=500
        )

@login_required
def cost_simulation_list(request):
    simulations = CostSimulation.objects.select_related('product').all()
    context = {
        'simulations': simulations,
    }
    return render(request, 'products/cost_simulation_list.html', context)

@login_required
def cost_simulation_create(request):
    if request.method == 'POST':
        form = CostSimulationForm(request.POST)
        if form.is_valid():
            simulation = form.save()
            return redirect('products:cost_simulation_detail', simulation_id=simulation.id)
    else:
        form = CostSimulationForm()
    context = {
        'form': form,
    }
    return render(request, 'products/cost_simulation_form.html', context)

@login_required
def cost_simulation_detail(request, simulation_id):
    simulation = get_object_or_404(CostSimulation, id=simulation_id)
    context = {
        'simulation': simulation,
    }
    return render(request, 'products/cost_simulation_detail.html', context)

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
    context = {
        'site': site,
        'equipment': equipment,
    }
    return render(request, 'products/equipment_list.html', context)

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
    context = {
        'form': form,
        'site': site,
    }
    return render(request, 'products/equipment_form.html', context)

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
    context = {
        'form': form,
        'site': equipment.site,
        'equipment': equipment,
    }
    return render(request, 'products/equipment_form.html', context)

@login_required
def equipment_delete(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    site = equipment.site
    if request.method == 'POST':
        equipment.delete()
        return redirect('products:equipment_list', site_id=site.id)
    context = {
        'equipment': equipment,
        'site': site,
    }
    return render(request, 'products/equipment_confirm_delete.html', context)