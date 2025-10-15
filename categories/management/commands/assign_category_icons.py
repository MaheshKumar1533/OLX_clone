from django.core.management.base import BaseCommand
from categories.models import Category


class Command(BaseCommand):
    help = 'Assign Font Awesome icons to categories'

    def handle(self, *args, **kwargs):
        # Mapping of category names/slugs to Font Awesome icons
        icon_mapping = {
            # Main Categories
            'academic-books': 'fas fa-book',
            'electronics-gadgets': 'fas fa-laptop',
            'fashion-accessories': 'fas fa-tshirt',
            'sports-fitness': 'fas fa-dumbbell',
            'musical-instruments': 'fas fa-music',
            'vehicles-transport': 'fas fa-car',
            'room-hostel-items': 'fas fa-bed',
            'project-lab-equipment': 'fas fa-flask',
            'gifts-collectibles': 'fas fa-gift',
            'health-personal-care': 'fas fa-heartbeat',
            'miscellaneous': 'fas fa-boxes',
            
            # Academic & Books
            'engineering-books': 'fas fa-cogs',
            'medical-books': 'fas fa-user-md',
            'mba-books': 'fas fa-briefcase',
            'science-books': 'fas fa-atom',
            'arts-literature': 'fas fa-feather-alt',
            'competitive-exam-books': 'fas fa-graduation-cap',
            'previous-year-papers': 'fas fa-file-alt',
            'study-notes': 'fas fa-sticky-note',
            
            # Electronics & Gadgets
            'laptops-computers': 'fas fa-laptop-code',
            'mobile-phones': 'fas fa-mobile-alt',
            'tablets-ipads': 'fas fa-tablet-alt',
            'headphones-audio': 'fas fa-headphones',
            'cameras': 'fas fa-camera',
            'smart-watches': 'fas fa-watch',
            'gaming-consoles': 'fas fa-gamepad',
            'calculators': 'fas fa-calculator',
            'software-licenses': 'fas fa-key',
            
            # Fashion & Accessories
            'casual-wear': 'fas fa-tshirt',
            'formal-wear': 'fas fa-user-tie',
            'ethnic-wear': 'fas fa-dharmachakra',
            'winter-wear': 'fas fa-mitten',
            'shoes-footwear': 'fas fa-shoe-prints',
            'bags-backpacks': 'fas fa-backpack',
            'watches': 'fas fa-clock',
            'jewelry-accessories': 'fas fa-gem',
            
            # Sports & Fitness
            'gym-equipment': 'fas fa-dumbbell',
            'yoga-fitness': 'fas fa-spa',
            'cricket-equipment': 'fas fa-baseball-ball',
            'football-basketball': 'fas fa-basketball-ball',
            'badminton-tennis': 'fas fa-table-tennis',
            'swimming-accessories': 'fas fa-swimmer',
            'cycling-gear': 'fas fa-biking',
            'outdoor-sports': 'fas fa-mountain',
            
            # Musical Instruments
            'guitars': 'fas fa-guitar',
            'keyboards-piano': 'fas fa-piano',
            'drums': 'fas fa-drum',
            'flutes-wind-instruments': 'fas fa-wind',
            'music-accessories': 'fas fa-compact-disc',
            'recording-equipment': 'fas fa-microphone',
            
            # Vehicles & Transport
            'bicycles': 'fas fa-bicycle',
            'electric-scooters': 'fas fa-charging-station',
            'skateboards': 'fas fa-skating',
            'helmets-safety-gear': 'fas fa-hard-hat',
            'vehicle-accessories': 'fas fa-tools',
            'travel-accessories': 'fas fa-suitcase-rolling',
            
            # Room & Hostel Items
            'mattresses-bedding': 'fas fa-bed',
            'study-desk-chair': 'fas fa-chair',
            'table-lamps': 'fas fa-lightbulb',
            'storage-organizers': 'fas fa-box-open',
            'curtains-decor': 'fas fa-palette',
            'kitchen-appliances': 'fas fa-blender',
            'mini-fridge': 'fas fa-icicles',
            'laundry-items': 'fas fa-soap',
            
            # Project & Lab Equipment
            'electronic-components': 'fas fa-microchip',
            'project-kits': 'fas fa-project-diagram',
            'lab-equipment': 'fas fa-vial',
            
            # Other Categories
            'college-merchandise': 'fas fa-university',
            'event-items': 'fas fa-calendar-alt',
            'stationery-supplies': 'fas fa-pen',
            'art-design-supplies': 'fas fa-paint-brush',
            'pet-accessories': 'fas fa-paw',
        }
        
        updated_count = 0
        for slug, icon in icon_mapping.items():
            try:
                category = Category.objects.get(slug=slug)
                category.icon = icon
                category.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Updated {category.name}: {icon}')
                )
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'✗ Category not found: {slug}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n{updated_count} categories updated with icons!')
        )
