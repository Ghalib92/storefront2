from django.core.management.base import BaseCommand
from store.models import Cart, CartItem, Product
import random


class Command(BaseCommand):
    help = 'Seed the database with sample shopping carts and items'

    def add_arguments(self, parser):
        parser.add_argument(
            '--carts',
            type=int,
            default=5,
            help='Number of carts to create (default: 5)'
        )

    def handle(self, *args, **options):
        num_carts = options['carts']
        
        # Get all available products
        products = list(Product.objects.all())
        
        if not products:
            self.stdout.write(self.style.ERROR(
                'No products found! Please run: python manage.py seed_products first'
            ))
            return

        # Clear existing carts
        deleted_count = Cart.objects.all().count()
        Cart.objects.all().delete()
        if deleted_count > 0:
            self.stdout.write(self.style.WARNING(
                f'Deleted {deleted_count} existing cart(s)'
            ))

        created_carts = 0
        created_items = 0

        # Create sample carts
        for i in range(num_carts):
            cart = Cart.objects.create()
            created_carts += 1
            
            # Add random number of items to each cart (1-8 items)
            num_items = random.randint(1, min(8, len(products)))
            selected_products = random.sample(products, num_items)
            
            for product in selected_products:
                # Random quantity between 1 and min(5, product inventory)
                max_quantity = min(5, product.inventory)
                if max_quantity > 0:
                    quantity = random.randint(1, max_quantity)
                    
                    CartItem.objects.create(
                        cart=cart,
                        product=product,
                        quantity=quantity
                    )
                    created_items += 1

            # Calculate and display cart summary
            total_items = sum(item.quantity for item in cart.items.all())
            total_price = sum(
                item.quantity * item.product.unit_price 
                for item in cart.items.all()
            )
            
            self.stdout.write(
                f'  Cart {i+1}: {cart.items.count()} products, '
                f'{total_items} total items, ${total_price:.2f}'
            )

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Successfully created {created_carts} cart(s) with {created_items} cart item(s)'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'✓ Cart IDs: {", ".join(str(cart.id)[:8] + "..." for cart in Cart.objects.all())}'
        ))
