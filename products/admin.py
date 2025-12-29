from django.contrib import admin
from .models import Category, Product, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'category', 'price', 'stock', 'featured']
    list_filter = ['category', 'created_at', 'featured']
    search_fields = ['name', 'description']
    list_editable = ['featured'] 

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']