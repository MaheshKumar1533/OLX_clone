from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Category
from products.models import Product

class CategoryListView(ListView):
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20

    def get_queryset(self):
        return Category.objects.filter(is_active=True, parent=None).order_by('name')

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'categories/category_detail.html'
    context_object_name = 'category'

    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs['slug'], is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        
        # Get products from this category and its subcategories
        subcategories = category.subcategories.filter(is_active=True)
        all_categories = [category] + list(subcategories)
        
        context['products'] = Product.objects.filter(
            category__in=all_categories,
            status='active'
        ).order_by('-created_at')[:20]
        
        context['subcategories'] = subcategories
        context['products_count'] = Product.objects.filter(
            category__in=all_categories,
            status='active'
        ).count()
        
        return context
