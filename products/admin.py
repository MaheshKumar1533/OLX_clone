from django.contrib import admin
from .models import Product, ProductImage, Wishlist, Contact

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'seller', 'city', 'status', 'is_featured', 'views_count', 'created_at']
    list_filter = ['status', 'condition', 'category', 'is_featured', 'is_negotiable', 'created_at', 'city']
    search_fields = ['title', 'description', 'seller__username', 'city']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    inlines = [ProductImageInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'category', 'seller')
        }),
        ('Price & Condition', {
            'fields': ('price', 'condition', 'is_negotiable')
        }),
        ('Location', {
            'fields': ('city', 'state', 'country')
        }),
        ('Product Details', {
            'fields': ('brand', 'model', 'status', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    list_editable = ['is_primary']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__title']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['product', 'buyer', 'seller', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['product__title', 'buyer__username', 'seller__username']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
