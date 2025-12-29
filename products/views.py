from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Product, Category, Review

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all().select_related('user')
    
    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1) if avg_rating else 0,
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        # Check if user already reviewed this product
        existing_review = Review.objects.filter(product=product, user=request.user).first()
        
        if existing_review:
            existing_review.rating = rating
            existing_review.comment = comment
            existing_review.save()
            messages.success(request, 'Review updated successfully!')
        else:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )
            messages.success(request, 'Review added successfully!')
        
        return redirect('product_detail', slug=product.slug)
    
    return redirect('product_detail', slug=product.slug)


