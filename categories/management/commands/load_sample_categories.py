from django.core.management.base import BaseCommand
from django.utils.text import slugify
from categories.models import Category

class Command(BaseCommand):
    help = 'Load sample categories'

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'Electronics',
                'description': 'Mobile phones, laptops, tablets, and other electronic devices',
                'subcategories': [
                    'Mobile Phones',
                    'Laptops & Computers',
                    'Tablets',
                    'Audio & Video',
                    'Gaming Consoles',
                    'Cameras',
                ]
            },
            {
                'name': 'Vehicles',
                'description': 'Cars, motorcycles, bicycles, and other vehicles',
                'subcategories': [
                    'Cars',
                    'Motorcycles',
                    'Bicycles',
                    'Auto Parts',
                    'Commercial Vehicles',
                ]
            },
            {
                'name': 'Home & Living',
                'description': 'Furniture, home decor, kitchen appliances, and household items',
                'subcategories': [
                    'Furniture',
                    'Home Decor',
                    'Kitchen Appliances',
                    'Home Improvement',
                    'Garden & Outdoor',
                ]
            },
            {
                'name': 'Fashion',
                'description': 'Clothing, shoes, accessories, and fashion items',
                'subcategories': [
                    'Men\'s Clothing',
                    'Women\'s Clothing',
                    'Shoes',
                    'Bags & Accessories',
                    'Watches',
                    'Jewelry',
                ]
            },
            {
                'name': 'Sports & Leisure',
                'description': 'Sports equipment, fitness gear, and leisure activities',
                'subcategories': [
                    'Fitness Equipment',
                    'Outdoor Sports',
                    'Team Sports',
                    'Water Sports',
                    'Indoor Games',
                ]
            },
            {
                'name': 'Books & Media',
                'description': 'Books, movies, music, and educational materials',
                'subcategories': [
                    'Books',
                    'Movies & TV Shows',
                    'Music',
                    'Educational Materials',
                ]
            },
            {
                'name': 'Services',
                'description': 'Professional services and business solutions',
                'subcategories': [
                    'Tutoring & Classes',
                    'Home Services',
                    'Professional Services',
                    'Event Services',
                ]
            },
            {
                'name': 'Others',
                'description': 'Miscellaneous items and everything else',
                'subcategories': [
                    'Baby & Kids',
                    'Pets & Accessories',
                    'Health & Beauty',
                    'Art & Collectibles',
                ]
            }
        ]

        for category_data in categories:
            # Create main category
            main_category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'slug': slugify(category_data['name']),
                    'description': category_data['description'],
                    'is_active': True,
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {main_category.name}')
                )
            
            # Create subcategories
            for subcategory_name in category_data['subcategories']:
                subcategory, created = Category.objects.get_or_create(
                    name=subcategory_name,
                    parent=main_category,
                    defaults={
                        'slug': slugify(subcategory_name),
                        'description': f'{subcategory_name} in {main_category.name}',
                        'is_active': True,
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created subcategory: {subcategory.name}')
                    )

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample categories!')
        )
