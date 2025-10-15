from django.core.management.base import BaseCommand
from categories.models import Category
from django.db import transaction


class Command(BaseCommand):
    help = 'Consolidate categories to a streamlined essential list'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('This will delete most categories. Make sure to backup your data!'))
        self.stdout.write('Starting category consolidation...\n')
        
        # Define essential categories for a college marketplace
        essential_categories = {
            'Books & Study Material': {
                'slug': 'books-study-material',
                'icon': 'fas fa-book',
                'description': 'Textbooks, notes, and study materials for all courses'
            },
            'Electronics & Gadgets': {
                'slug': 'electronics-gadgets',
                'icon': 'fas fa-laptop',
                'description': 'Laptops, phones, tablets, and electronic accessories'
            },
            'Fashion & Accessories': {
                'slug': 'fashion-accessories',
                'icon': 'fas fa-tshirt',
                'description': 'Clothing, shoes, bags, and fashion accessories'
            },
            'Sports & Fitness': {
                'slug': 'sports-fitness',
                'icon': 'fas fa-dumbbell',
                'description': 'Sports equipment, gym gear, and fitness accessories'
            },
            'Room & Furniture': {
                'slug': 'room-furniture',
                'icon': 'fas fa-couch',
                'description': 'Furniture, mattresses, and room essentials'
            },
            'Vehicles & Transport': {
                'slug': 'vehicles-transport',
                'icon': 'fas fa-bicycle',
                'description': 'Bicycles, bikes, and transport accessories'
            },
            'Musical Instruments': {
                'slug': 'musical-instruments',
                'icon': 'fas fa-guitar',
                'description': 'Guitars, keyboards, and other musical instruments'
            },
            'Lab & Project Equipment': {
                'slug': 'lab-project-equipment',
                'icon': 'fas fa-flask',
                'description': 'Lab equipment, project kits, and technical supplies'
            },
            'Art & Stationery': {
                'slug': 'art-stationery',
                'icon': 'fas fa-paint-brush',
                'description': 'Art supplies, stationery, and creative materials'
            },
            'Miscellaneous': {
                'slug': 'miscellaneous',
                'icon': 'fas fa-boxes',
                'description': 'Other items that don\'t fit in above categories'
            },
        }
        
        with transaction.atomic():
            # Get all existing categories
            existing_categories = list(Category.objects.all())
            self.stdout.write(f'Found {len(existing_categories)} existing categories\n')
            
            # Create or update essential categories
            created_count = 0
            updated_count = 0
            
            for name, data in essential_categories.items():
                category, created = Category.objects.update_or_create(
                    slug=data['slug'],
                    defaults={
                        'name': name,
                        'description': data['description'],
                        'icon': data['icon'],
                        'is_active': True,
                        'parent': None
                    }
                )
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'✓ Created: {name}'))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f'✓ Updated: {name}'))
            
            # Get slugs of essential categories
            essential_slugs = [data['slug'] for data in essential_categories.values()]
            
            # Delete all categories that are not in the essential list
            deleted_count = Category.objects.exclude(slug__in=essential_slugs).delete()[0]
            
            self.stdout.write(self.style.SUCCESS(f'\n✅ Consolidation complete!'))
            self.stdout.write(f'  Created: {created_count}')
            self.stdout.write(f'  Updated: {updated_count}')
            self.stdout.write(f'  Deleted: {deleted_count}')
            self.stdout.write(f'  Total categories now: {Category.objects.count()}')
