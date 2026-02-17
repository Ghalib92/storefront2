from rest_framework import serializers
from .models import Cart, CartItem, Customer, Product, Collection, Review
from decimal import Decimal


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
    products_count = serializers.IntegerField(read_only=True)    

class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'collection', 'price_with_tax']
    
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
         view_name='collection-detail'
     )  # Nested serializer, creates a relationship between the two serializers
    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'rating', 'created_at']
    
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    """Simplified product serializer for cart items"""
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']
    
    def get_total_price(self, item: CartItem):
        return item.quantity * item.product.unit_price
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Product does not exist')
        return value
    
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError('Quantity must be at least 1')
        return value
    
    def create(self, validated_data):
        cart_id = self.context['cart_id']
        product_id = validated_data['product_id']
        quantity = validated_data['quantity']
        
        # Check if product has sufficient inventory
        product = Product.objects.get(pk=product_id)
        if product.inventory < quantity:
            raise serializers.ValidationError('Insufficient inventory')
        
        # Check if item already exists in cart
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            # Update quantity if item exists
            cart_item.quantity += quantity
            if product.inventory < cart_item.quantity:
                raise serializers.ValidationError('Insufficient inventory')
            cart_item.save()
            return cart_item
        except CartItem.DoesNotExist:
            # Create new item
            return CartItem.objects.create(cart_id=cart_id, **validated_data)
    
    def update(self, instance, validated_data):
        quantity = validated_data.get('quantity', instance.quantity)
        
        # Check inventory
        if instance.product.inventory < quantity:
            raise serializers.ValidationError('Insufficient inventory')
        
        instance.quantity = quantity
        instance.save()
        return instance


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items', 'total_price', 'total_items']
        read_only_fields = ['id', 'created_at']
    
    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    
    def get_total_items(self, cart: Cart):
        return sum([item.quantity for item in cart.items.all()]) 
    


class CustomerSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id','user_id', 'first_name', 'last_name', 'email', 'phone', 'birth_date', 'membership']    