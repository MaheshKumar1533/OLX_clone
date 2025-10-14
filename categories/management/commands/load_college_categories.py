from django.core.management.base import BaseCommand
from django.utils.text import slugify
from categories.models import Category

class Command(BaseCommand):
    help = 'Load college-specific categories for STUDYSWAP'

    def handle(self, *args, **options):
        # Clear existing categories
        Category.objects.all().delete()
        
        categories = [
            {
                'name': 'Academic & Books',
                'description': 'Textbooks, reference books, notes, and study materials for all subjects',
                'subcategories': [
                    'Engineering Books',
                    'Medical Books',
                    'MBA Books',
                    'Arts & Literature',
                    'Science Books',
                    'Competitive Exam Books',
                    'Study Notes',
                    'Previous Year Papers',
                ]
            },
            {
                'name': 'Electronics & Gadgets',
                'description': 'Laptops, phones, tablets, calculators, and other electronic devices',
                'subcategories': [
                    'Laptops & Computers',
                    'Mobile Phones',
                    'Tablets & iPads',
                    'Calculators',
                    'Headphones & Audio',
                    'Cameras',
                    'Gaming Consoles',
                    'Smart Watches',
                ]
            },
            {
                'name': 'Room & Hostel Items',
                'description': 'Furniture, appliances, and essentials for dorm rooms and hostels',
                'subcategories': [
                    'Mattresses & Bedding',
                    'Study Desk & Chair',
                    'Storage & Organizers',
                    'Mini Fridge',
                    'Table Lamps',
                    'Curtains & Decor',
                    'Kitchen Appliances',
                    'Laundry Items',
                ]
            },
            {
                'name': 'Fashion & Accessories',
                'description': 'Clothing, shoes, bags, and accessories for college life',
                'subcategories': [
                    'Casual Wear',
                    'Formal Wear',
                    'Shoes & Footwear',
                    'Bags & Backpacks',
                    'Watches',
                    'Jewelry & Accessories',
                    'Winter Wear',
                    'Ethnic Wear',
                ]
            },
            {
                'name': 'Sports & Fitness',
                'description': 'Sports equipment, gym gear, and fitness accessories',
                'subcategories': [
                    'Cricket Equipment',
                    'Badminton & Tennis',
                    'Football & Basketball',
                    'Gym Equipment',
                    'Cycling Gear',
                    'Swimming Accessories',
                    'Yoga & Fitness',
                    'Outdoor Sports',
                ]
            },
            {
                'name': 'Musical Instruments',
                'description': 'Guitars, keyboards, and other musical instruments',
                'subcategories': [
                    'Guitars',
                    'Keyboards & Piano',
                    'Drums',
                    'Flutes & Wind Instruments',
                    'Music Accessories',
                    'Recording Equipment',
                ]
            },
            {
                'name': 'Vehicles & Transport',
                'description': 'Bicycles, scooters, and other transportation for campus life',
                'subcategories': [
                    'Bicycles',
                    'Electric Scooters',
                    'Skateboards',
                    'Vehicle Accessories',
                    'Helmets & Safety Gear',
                ]
            },
            {
                'name': 'Project & Lab Equipment',
                'description': 'Tools, components, and equipment for college projects',
                'subcategories': [
                    'Electronic Components',
                    'Lab Equipment',
                    'Project Kits',
                    'Software & Licenses',
                    'Stationery & Supplies',
                    'Art & Design Supplies',
                ]
            },
            {
                'name': 'Miscellaneous',
                'description': 'Everything else that doesn\'t fit in other categories',
                'subcategories': [
                    'Gifts & Collectibles',
                    'Event Items',
                    'Travel Accessories',
                    'Health & Personal Care',
                    'Pet Accessories',
                    'College Merchandise',
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
                        'description': f'{subcategory_name} for college students',
                        'is_active': True,
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created subcategory: {subcategory.name}')
                    )

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded college-specific categories for STUDYSWAP!')
        )
