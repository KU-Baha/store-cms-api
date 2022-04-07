from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import (
    ProductSerializer,
    ChildrenProductSerializer
)
from .models import (
    Product,
    ChildrenProduct
)


class ProductViewSet(viewsets.ModelViewSet):
    """
    Продукт
    Реализованы все базовые методы ModelViewSet
    Реализован свой метод similar для получение похожих товаров
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(deleted=False)

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
    """
    serializer_class = ChildrenProductSerializer
    queryset = ChildrenProduct.objects.filter(deleted=False)

    def destroy(self, request, pk=None):
        queryset = get_object_or_404(ChildrenProduct, pk=pk)
        queryset.deleted = True
        queryset.save()
        return Response('Успешно удален!', status=status.HTTP_200_OK)