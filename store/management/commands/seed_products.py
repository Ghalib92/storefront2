from django.core.management.base import BaseCommand
from decimal import Decimal
from store.models import Collection, Product


class Command(BaseCommand):
    help = 'Seed the database with sample products'

    def handle(self, *args, **options):
        # Create or get collections
        electronics, _ = Collection.objects.get_or_create(
            title='Electronics',
            defaults={'title': 'Electronics'}
        )
        clothing, _ = Collection.objects.get_or_create(
            title='Clothing',
            defaults={'title': 'Clothing'}
        )
        books, _ = Collection.objects.get_or_create(
            title='Books',
            defaults={'title': 'Books'}
        )

        # Sample products data
        products_data = [
            {
                'title': 'Laptop Pro',
                'slug': 'laptop-pro',
                'description': 'High-performance laptop for professionals',
                'unit_price': Decimal('1299.99'),
                'inventory': 15,
                'collection': electronics
            },
            {
                'title': 'Wireless Mouse',
                'slug': 'wireless-mouse',
                'description': 'Ergonomic wireless mouse with long battery life',
                'unit_price': Decimal('29.99'),
                'inventory': 50,
                'collection': electronics
            },
            {
                'title': 'USB-C Cable',
                'slug': 'usb-c-cable',
                'description': 'Fast charging USB-C cable',
                'unit_price': Decimal('12.99'),
                'inventory': 100,
                'collection': electronics
            },
            {
                'title': 'Cotton T-Shirt',
                'slug': 'cotton-tshirt',
                'description': '100% organic cotton comfortable t-shirt',
                'unit_price': Decimal('19.99'),
                'inventory': 75,
                'collection': clothing
            },
            {
                'title': 'Denim Jeans',
                'slug': 'denim-jeans',
                'description': 'Classic blue denim jeans',
                'unit_price': Decimal('59.99'),
                'inventory': 40,
                'collection': clothing
            },
            {
                'title': 'Django for Beginners',
                'slug': 'django-for-beginners',
                'description': 'Learn Django web development from scratch',
                'unit_price': Decimal('39.99'),
                'inventory': 25,
                'collection': books
            },
            {
                'title': 'Python Cookbook',
                'slug': 'python-cookbook',
                'description': 'Recipes and solutions for Python programmers',
                'unit_price': Decimal('44.99'),
                'inventory': 30,
                'collection': books
            },
            {
                'title': 'Mechanical Keyboard',
                'slug': 'mechanical-keyboard',
                'description': 'RGB mechanical keyboard with tactile switches',
                'unit_price': Decimal('129.99'),
                'inventory': 20,
                'collection': electronics
            },
        ]

        # Create products
        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults=product_data
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} products'
            )
        )
