from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    ProductSerializer,
    ChildrenProductSerializer,
    CollectionSerializer
)
from .models import (
    Product,
    ChildrenProduct,
    Collection
)


class ProductViewSet(viewsets.ModelViewSet):
    """
    Продукт
    Реализованы все базовые методы ModelViewSet
    Реализован свой метод similar для получение похожих товаров
    Поиск по названию
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(deleted=False)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name', )

    def similar(self, request, pk=None, qt=None):
        """
        Получение похожих товаров
        """
        queryset = Product.objects.filter(collection_id=pk, deleted=False)[0:qt]
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = Product.objects.get(pk=pk)
        queryset.deleted = True
        queryset.save()
        return Response('Успешно удален!', status=status.HTTP_200_OK)


class ChildrenProductViewSet(viewsets.ModelViewSet):
    """
    Подпродукт
    Реализованы все базовые методы ModelViewSet кроме destroy
    """
    serializer_class = ChildrenProductSerializer
    queryset = ChildrenProduct.objects.filter(deleted=False)

    def destroy(self, request, pk=None):
        queryset = get_object_or_404(ChildrenProduct, pk=pk)
        queryset.deleted = True
        queryset.save()
        return Response('Успешно удален!', status=status.HTTP_200_OK)


class CollectionViewSet(viewsets.ModelViewSet):
    """
    Коллекция
    """
    serializer_class = CollectionSerializer
    queryset = Collection.objects.filter(deleted=False)

    def destroy(self, request, pk=None):
        queryset = get_object_or_404(Collection, pk=pk)
        queryset.deleted = True
        queryset.save()
        return Response('Успешно удален!', status=status.HTTP_200_OK)

