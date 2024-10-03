from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, ProductRange
from .forms import ProductForm

@login_required
def dashboard(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'products/dashboard.html', context)

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