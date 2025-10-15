from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.ProductSearchView.as_view(), name='search'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/<slug:slug>/edit/', views.ProductEditView.as_view(), name='product_edit'),
    path('product/<slug:slug>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('wishlist/add/<int:product_id>/', views.AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
]
