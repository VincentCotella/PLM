from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Product, ProductRange, Site, Project, ModificationHistory
from .forms import ProductForm
from django.shortcuts import redirect

@login_required
def dashboard(request):
    products = Product.objects.all()
    ranges = ProductRange.objects.all()
    sites = Site.objects.all()
    projects = Project.objects.all()
    modifications = ModificationHistory.objects.all()

    # Récupérer les widgets sélectionnés depuis l'URL ou utiliser la liste par défaut
    selected_widgets = request.GET.getlist('widgets', [
        'overview', 'product_ranges', 'production_sites', 'product_categories',
        'recent_modifications', 'active_projects', 'cost_simulations',
        'modification_history', 'generate_report'
    ])

    context = {
        'products': products,
        'ranges': ranges,
        'sites': sites,
        'projects': projects,
        'agrifood_products': products.filter(product_range__category='AG'),
        'perfumery_products': products.filter(product_range__category='PE'),
        'modification_history': modifications,
        'selected_widgets': selected_widgets
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