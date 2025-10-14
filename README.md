# STUDYSWAP - Django Marketplace Application

A full-featured marketplace application built with Django, where users can buy and sell products through a modern, intuitive platform.

## Features

### User Features

- User registration and authentication
- User profiles with personal information
- Password reset functionality
- Product listing with multiple images
- Product search and filtering
- Category-based browsing
- Wishlist functionality
- Contact seller messaging
- Personal dashboard with user's products

### Product Features

- Multiple product categories and subcategories
- Image upload support
- Product condition tracking
- Price negotiation options
- Location-based listing
- Product status management (Active/Sold/Inactive)
- View count tracking
- Featured products

### Admin Features

- Django admin interface
- User and product management
- Category management
- Contact message handling
- Analytics and reporting

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Forms**: Django Crispy Forms with Bootstrap 5
- **Images**: Pillow for image processing
- **Configuration**: Python Decouple for environment variables

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**

   ```bash
   cd /home/mahi/Projects/OLX_clone
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment variables**

   - The `.env` file is already configured with default settings
   - For production, update the settings in `.env` file

4. **Run migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Load sample data**

   ```bash
   python manage.py load_sample_categories
   ```

6. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**

   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
STUDYSWAP/
├── accounts/              # User authentication and profiles
├── categories/            # Product categories management
├── products/             # Product listings and search
├── static/               # CSS, JS, images
├── templates/            # HTML templates
├── media/                # User uploaded files
├── olx_clone/           # Main Django project settings
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables
└── manage.py            # Django management script
```

## Key Models

### User Profile

- Extended user model with profile information
- Phone, address, profile image
- Automatic profile creation on user registration

### Categories

- Hierarchical category structure (parent/child)
- Category slugs for SEO-friendly URLs
- Active/inactive status

### Products

- Complete product information
- Multiple image support
- Status tracking (Active/Sold/Inactive)
- Location information
- View count and timestamps

### Additional Models

- ProductImage: Multiple images per product
- Wishlist: User's saved products
- Contact: Buyer-seller communication

## Usage Guide

### For Users

1. **Registration**: Create account with email verification
2. **Profile Setup**: Complete profile with contact information
3. **Browse Products**: Use search filters and categories
4. **Post Ads**: Create product listings with images
5. **Manage Listings**: Edit, delete, or mark as sold
6. **Communication**: Contact sellers through built-in messaging

### For Admins

1. **Access Admin Panel**: Use superuser credentials
2. **Manage Categories**: Add/edit product categories
3. **User Management**: View user profiles and activity
4. **Content Moderation**: Review and manage product listings
5. **Analytics**: Monitor site activity and user engagement

## Customization

### Adding New Features

- Extend models in respective apps
- Create new views and templates
- Update URL configurations
- Add corresponding admin interfaces

### Styling

- Modify CSS in `static/css/style.css`
- Update Bootstrap themes
- Customize templates in `templates/` directory

### Configuration

- Update settings in `olx_clone/settings.py`
- Modify environment variables in `.env`
- Configure email settings for notifications

## Production Deployment

### Database

- Switch from SQLite to PostgreSQL/MySQL
- Update database settings in settings.py

### Static Files

- Configure static file serving with nginx/Apache
- Set up media file handling
- Enable compression and caching

### Security

- Use strong SECRET_KEY
- Set DEBUG=False
- Configure ALLOWED_HOSTS
- Set up HTTPS/SSL
- Implement security headers

### Performance

- Enable database query optimization
- Set up caching (Redis/Memcached)
- Optimize images and static files
- Configure CDN for static assets

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with proper testing
4. Submit pull request with detailed description

## Support

For issues and questions:

- Check existing documentation
- Review Django documentation
- Create issue in repository
- Contact project maintainers

## License

This project is open source and available under the MIT License.

## Version History

- **v1.0.0**: Initial release with core marketplace functionality
  - User authentication and profiles
  - Product listing and search
  - Category management
  - Basic admin interface
  - Responsive design with Bootstrap 5
