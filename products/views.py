from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
)
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from .models import Product, ProductImage, Wishlist, Contact
from .forms import ProductForm, ProductSearchForm
from categories.models import Category

class HomeView(ListView):
    model = Product
    template_name = 'products/home.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(status='active').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(
            status='active', is_featured=True
        ).order_by('-created_at')[:8]
        context['categories'] = Category.objects.filter(is_active=True, parent=None)[:8]
        context['search_form'] = ProductSearchForm()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_object(self):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        # Increment view count
        product.increment_views()
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Related products from the same category
        context['related_products'] = Product.objects.filter(
            category=product.category,
            status='active'
        ).exclude(id=product.id).order_by('-created_at')[:6]
        
                # Check if product is in user's wishlist
        if self.request.user.is_authenticated:
            context['in_wishlist'] = Wishlist.objects.filter(
                user=self.request.user,
                product=product
            ).exists()
        else:
            context['in_wishlist'] = False
        
        return context

class ProductSearchView(ListView):
    model = Product
    template_name = 'products/search_results.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        form = ProductSearchForm(self.request.GET)
        queryset = Product.objects.filter(status='active')

        if form.is_valid():
            query = form.cleaned_data.get('query')
            category = form.cleaned_data.get('category')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            city = form.cleaned_data.get('city')
            condition = form.cleaned_data.get('condition')

            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(brand__icontains=query) |
                    Q(model__icontains=query)
                )

            if category:
                queryset = queryset.filter(category=category)

            if min_price:
                queryset = queryset.filter(price__gte=min_price)

            if max_price:
                queryset = queryset.filter(price__lte=max_price)

            if city:
                queryset = queryset.filter(city__icontains=city)

            if condition:
                queryset = queryset.filter(condition=condition)

        # Apply sorting
        sort_by = self.request.GET.get('sort_by', '')
        if sort_by == 'price_low':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort_by == 'title_asc':
            queryset = queryset.order_by('title')
        elif sort_by == 'title_desc':
            queryset = queryset.order_by('-title')
        else:
            # Default: Most recent first
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ProductSearchForm(self.request.GET)
        context['query'] = self.request.GET.get('query', '')
        context['sort_by'] = self.request.GET.get('sort_by', '')
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'

    def form_valid(self, form):
        form.instance.seller = self.request.user
        response = super().form_valid(form)
        
        # Handle multiple image uploads
        images = self.request.FILES.getlist('images')
        for i, image in enumerate(images):
            ProductImage.objects.create(
                product=self.object,
                image=image,
                is_primary=(i == 0)  # First image is primary
            )
        
        messages.success(self.request, 'Product listed successfully!')
        return response

    def get_success_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.object.slug})

class ProductEditView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Handle new image uploads
        images = self.request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(
                product=self.object,
                image=image
            )
        
        messages.success(self.request, 'Product updated successfully!')
        return response

    def get_success_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.object.slug})

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('accounts:my_products')

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Product deleted successfully!')
        return super().delete(request, *args, **kwargs)

class AddToWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, status='active')
        
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if created:
            messages.success(request, f'{product.title} added to your wishlist!')
        else:
            messages.info(request, f'{product.title} is already in your wishlist!')
        
        return redirect('products:product_detail', slug=product.slug)

class RemoveFromWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        
        try:
            wishlist_item = Wishlist.objects.get(user=request.user, product=product)
            wishlist_item.delete()
            messages.success(request, f'{product.title} removed from your wishlist!')
        except Wishlist.DoesNotExist:
            messages.error(request, 'Product not found in your wishlist!')
        
        return redirect('products:product_detail', slug=product.slug)
