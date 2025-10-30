from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Product


class Command(BaseCommand):
    help = 'Generate slugs for products that don\'t have them'

    def handle(self, *args, **kwargs):
        products_without_slugs = Product.objects.filter(slug='')
        count = 0
        
        for product in products_without_slugs:
            product.slug = slugify(product.title)
            # Ensure unique slug
            original_slug = product.slug
            num = 1
            while Product.objects.filter(slug=product.slug).exclude(id=product.id).exists():
                product.slug = f"{original_slug}-{num}"
                num += 1
            product.save()
            count += 1
            self.stdout.write(f'Fixed slug for product: {product.title} -> {product.slug}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully fixed {count} product slugs'))
