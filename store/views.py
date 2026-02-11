from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . models import Product, Collection
from . serializers import ProductSerializer, CollectionSerializer
# Create your views here.

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    queryset = Product.objects.select_related('collection').all()
    serializer = ProductSerializer(queryset, many = True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    if request.method == 'PUT':
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        product = get_object_or_404(Product, pk=id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product, context={'request': request})
    return Response(serializer.data)
   
@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    queryset = Collection.objects.all()
    serializer = CollectionSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if collection.product_set.count() > 0:
            return Response(
                {'error': 'Cannot delete collection with associated products'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)