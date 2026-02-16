from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

# Main router for top-level resources
router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('collections', views.CollectionViewSet, basename='collection')

# Nested router for products under collections
# Example: /collections/{collection_pk}/products/
collections_router = routers.NestedDefaultRouter(router, 'collections', lookup='collection')
collections_router.register('products', views.ProductViewSet, basename='collection-products')

# Nested router for reviews under products
# Example: /products/{product_pk}/reviews/
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(collections_router.urls)),
    path('', include(products_router.urls)),
]