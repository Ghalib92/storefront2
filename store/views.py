from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
# from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Product, Collection, Review, Cart, CartItem, Customer
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, CustomerSerializer
 
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
# Create your views here.



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['collection_id']
 
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_updated']

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     # Support for nested route: /collections/{collection_pk}/products/
    #     collection_pk = self.kwargs.get('collection_pk')
    #     if collection_pk is not None:
    #         queryset = queryset.filter(collection_id=collection_pk)
    #     return queryset

    def get_serializer_context(self):
        return {'request': self.request}
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orders_count > 0:
            return Response(
                {'error': 'Cannot delete product with associated orders'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    

# class ProductList(ListCreateAPIView) :

#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

 
#     def get_serializer_context(self):
#         return {'request': self.request}

    
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'id'

    # def put(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     serializer = ProductSerializer(product, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = CollectionSerializer
    lookup_field = 'pk'

    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('product')), pk=pk)
        if collection.products_count > 0:
            return Response(
                {'error': 'Cannot delete collection with associated products'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('product')).all()
#     serializer_class = CollectionSerializer


# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('product')).all()
#     serializer_class = CollectionSerializer
#     lookup_field = 'pk'   
 
# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, pk):
#     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('product')), pk=pk)
#     if request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         if collection.products_count > 0:
#             return Response(
#                 {'error': 'Cannot delete collection with associated products'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED
#             )
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     serializer = CollectionSerializer(collection)
#     return Response(serializer.data)


class CartViewSet(ModelViewSet):
    """
    ViewSet for managing shopping carts.
    
    Endpoints:
    - GET /carts/ - List all carts
    - POST /carts/ - Create a new cart
    - GET /carts/{id}/ - Retrieve a cart
    - DELETE /carts/{id}/ - Delete a cart (clear cart)
    """
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    lookup_field = 'pk'

    @action(detail=True, methods=['post'])
    def clear(self, request, pk=None):
        """Clear all items from the cart"""
        cart = self.get_object()
        cart.items.all().delete()
        return Response({'message': 'Cart cleared successfully'}, status=status.HTTP_204_NO_CONTENT)


class CartItemViewSet(ModelViewSet):
    """
    ViewSet for managing cart items.
    
    Endpoints:
    - GET /carts/{cart_pk}/items/ - List all items in cart
    - POST /carts/{cart_pk}/items/ - Add item to cart
    - GET /carts/{cart_pk}/items/{id}/ - Retrieve a cart item
    - PATCH/PUT /carts/{cart_pk}/items/{id}/ - Update item quantity
    - DELETE /carts/{cart_pk}/items/{id}/ - Remove item from cart
    """
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}


class CustomerViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer