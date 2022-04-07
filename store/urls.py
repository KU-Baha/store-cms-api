from django.urls import path
from .views import (
    ProductViewSet,
    ChildrenProductViewSet,
    CollectionViewSet
)
urlpatterns = [
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('product/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update',
                                                      'delete': 'destroy'})),
    path('similar-products/<int:pk>/<int:qt>/', ProductViewSet.as_view({'get': 'similar'})),

    path('children-products/', ChildrenProductViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('children-product/<int:pk>/', ChildrenProductViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                                       'delete': 'destroy', 'patch': 'partial_update'})),
    path('collections/', CollectionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('collection/<int:pk>/', CollectionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy',
                                                            'patch': 'partial_update'})),
]

