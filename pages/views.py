# Add this import at the top
from django.shortcuts import render
from products.models import Product

# Update your home view function
def home(request):
    featured_products = Product.objects.filter(featured=True, stock__gt=0)[:4]  # Get up to 4 featured products
    context = {
        'featured_products': featured_products
    }
    return render(request, 'pages/home.html', context)