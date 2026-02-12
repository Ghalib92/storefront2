from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet    
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from . models import Product, Collection
from . serializers import ProductSerializer, CollectionSerializer
# Create your views here.



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

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