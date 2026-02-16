from django.core.management.base import BaseCommand
from store.models import Product, Review
import random


class Command(BaseCommand):
    help = 'Seed the database with sample reviews for products'

    def handle(self, *args, **options):
        # Sample review data
        review_templates = [
            {
                'names': ['John Smith', 'Sarah Johnson', 'Mike Williams', 'Emily Davis', 'David Brown'],
                'positive': [
                    'Excellent product! Exceeded my expectations.',
                    'Really impressed with the quality. Highly recommend!',
                    'Great value for money. Very satisfied with my purchase.',
                    'Outstanding quality and fast delivery. Will buy again!',
                    'Perfect! Exactly what I was looking for.',
                ],
                'neutral': [
                    'Good product overall. Does what it says.',
                    'Decent quality for the price. No complaints.',
                    'Works as expected. Nothing special but solid.',
                    'It\'s okay. Met my basic needs.',
                ],
                'negative': [
                    'Not as good as expected. A bit disappointing.',
                    'Could be better. Had some issues with it.',
                    'Average quality. Expected more for the price.',
                ]
            }
        ]

        names = ['John Smith', 'Sarah Johnson', 'Mike Williams', 'Emily Davis', 'David Brown',
                 'Lisa Anderson', 'Tom Wilson', 'Jennifer Lee', 'Chris Martin', 'Amanda Taylor',
                 'Robert Garcia', 'Michelle Martinez', 'Kevin Rodriguez', 'Jessica Hernandez',
                 'Daniel Lopez', 'Laura Gonzalez', 'Ryan Perez', 'Nicole Moore', 'James Wilson']

        positive_reviews = [
            'Excellent product! Exceeded my expectations.',
            'Really impressed with the quality. Highly recommend!',
            'Great value for money. Very satisfied with my purchase.',
            'Outstanding quality and fast delivery. Will buy again!',
            'Perfect! Exactly what I was looking for.',
            'Best purchase I\'ve made in a while!',
            'Absolutely love it! Five stars all the way.',
            'Superior quality and great customer service.',
            'Fantastic product, would definitely recommend to friends.',
            'Worth every penny. Very happy with this purchase.',
        ]

        neutral_reviews = [
            'Good product overall. Does what it says.',
            'Decent quality for the price. No complaints.',
            'Works as expected. Nothing special but solid.',
            'It\'s okay. Met my basic needs.',
            'Reasonable quality. Good enough for everyday use.',
            'Fair product. Gets the job done.',
        ]

        negative_reviews = [
            'Not as good as expected. A bit disappointing.',
            'Could be better. Had some issues with it.',
            'Average quality. Expected more for the price.',
            'Not worth the money in my opinion.',
            'Had higher expectations based on reviews.',
        ]

        products = Product.objects.all()
        
        if not products.exists():
            self.stdout.write(
                self.style.ERROR('No products found. Please run seed_products first.')
            )
            return

        created_count = 0
        
        for product in products:
            # Random number of reviews per product (2-5)
            num_reviews = random.randint(2, 5)
            
            for _ in range(num_reviews):
                rating = random.randint(1, 5)
                
                # Choose review text based on rating
                if rating >= 4:
                    description = random.choice(positive_reviews)
                elif rating == 3:
                    description = random.choice(neutral_reviews)
                else:
                    description = random.choice(negative_reviews)
                
                name = random.choice(names)
                
                # Create review (avoid duplicates)
                review, created = Review.objects.get_or_create(
                    product=product,
                    name=name,
                    description=description,
                    defaults={'rating': rating}
                )
                
                if created:
                    created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} reviews across {products.count()} products'
            )
        )
