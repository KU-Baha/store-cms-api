from django.urls import path
from .views import (
    ProductViewSet,
    ChildrenProductViewSet,
    CollectionViewSet,
    OrderViewSet,
    OrderItemViewSet,
    CustomerViewSet,
    CartViewSet
)

urlpatterns = [
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('product/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update',
                                                      'delete': 'destroy'})),
    path('similar-products/<int:pk>/<int:qt>/', ProductViewSet.as_view({'get': 'similar'})),
    path('bestsellers/<int:qt>/', ProductViewSet.as_view({'get': 'bestsellers'})),
    path('novelties/<int:qt>/', ProductViewSet.as_view({'get': 'novelties'})),

    path('children-products/', ChildrenProductViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('children-product/<int:pk>/', ChildrenProductViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                                       'delete': 'destroy', 'patch': 'partial_update'})),
    path('collections/', CollectionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('collection/<int:pk>/', CollectionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy',
                                                            'patch': 'partial_update'})),

    path('order/', OrderViewSet.as_view({'post': 'create'})),
    path('order/<int:pk>/', OrderViewSet.as_view({'get': 'retrieve'})),
    path('order/<int:pk>/items/', OrderItemViewSet.as_view({'get': 'list'})),
    path('order/item/<int:pk>/', OrderItemViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('customer/<int:pk>/', CustomerViewSet.as_view({'get': 'retrieve'})),
    path('cart/<int:pk>/', CartViewSet.as_view({'get': 'retrieve', 'post': 'add_item', 'put': 'update_item', 'delete': 'delete_item'}))
]

