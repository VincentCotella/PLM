from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Product, ProductRange, Site, Project, ModificationHistory
from .forms import ProductForm
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

    # Serialize QuerySets into lists of dictionaries
    agrifood_products_data = list(
        products.filter(product_range__category='AG').values('id', 'name')
    )
    perfumery_products_data = list(
        products.filter(product_range__category='PE').values('id', 'name')
    )

    cost_simulations_data = []
    for product in products:
        simulations = product.cost_simulations.all()
        for simulation in simulations:
            cost_simulations_data.append({
                'product_name': product.name,
                'calculated_price': float(simulation.calculated_price),
            })

    context = {
        'products': products,
        'ranges': ranges,
        'sites': sites,
        'projects': projects,
        'agrifood_products_data': json.dumps(agrifood_products_data, cls=DjangoJSONEncoder),
        'perfumery_products_data': json.dumps(perfumery_products_data, cls=DjangoJSONEncoder),
        'cost_simulations_data': json.dumps(cost_simulations_data, cls=DjangoJSONEncoder),
        'modification_history': modification_history,
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