from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    ProductSerializer,
    ChildrenProductSerializer,
    CollectionSerializer,
    OrderSerializer,
    OrderItemSerializer,
)
from .models import (
    Product,
    ChildrenProduct,
    Collection,
    Order,
    OrderItem,
)


class ProductViewSet(viewsets.ModelViewSet):
    """
    Продукт
    Реализованы все базовые методы ModelViewSet, переделан destroy
    Реализован свой метод similar для получение похожих товаров
    Реализован свой метод bestsellers для получение товаров со статусом "Хит продаж"
    Реализован свой метод novelties для получение товаров со статусом "Новый"
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

    def bestsellers(self, request, qt=None):
        """
        Получение товаров со статусом "Хит продаж"
        """
        queryset = self.filter_queryset(Product.objects.filter(deleted=False, bestseller=True)[0:qt])
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def novelties(self, request, qt=None):
        """
        Получение товаров сос статусом "Новинки"
        """
        queryset = self.filter_queryset(Product.objects.filter(deleted=False, novelty=True)[0:qt])
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ChildrenProductViewSet(viewsets.ModelViewSet):
    """
    Подпродукт
    Реализованы все базовые методы ModelViewSet, переделан destroy
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
    Реализованы все базовые методы ModelViewSet, переделан destroy
    """
    serializer_class = CollectionSerializer
    queryset = Collection.objects.filter(deleted=False)

    def destroy(self, request, pk=None):
        queryset = get_object_or_404(Collection, pk=pk)
        queryset.deleted = True
        queryset.save()
        return Response('Успешно удален!', status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ModelViewSet):
    """
    Заказ
    Реализованы все базовые методы ModelViewSet, переделан create
            Пример API для создания
        {
        "user_data": {
            "first_name": "Name",
            "last_name": "Surname",
            "mail": "mail@gmail.com",
            "phone_number": "+996 999 999",
            "country": "Kyrgystan",
            "city": "Bishkek"
        },
        "products": [
                {
                "id": 1,
                "quantity": 2
                },
                {
                "id": 2,
                "quantity": 1
                }
                ]
        }
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.filter(deleted=False)

    def create(self, request, *args, **kwargs):
        try:
            order = Order.objects.create(**request.data['user_data'])
            for data in request.data['products']:
                if ChildrenProduct.objects.get(id=data['id']).amount < data['quantity']:
                    raise Exception('На складе меньше товаров, чем вы запросили!')
                OrderItem.objects.create(children_product_id=data['id'], quantity=data['quantity'], order=order)
        except Exception as e:
            return Response(f'Ошибка при обработке заказа! Ошибка {e}', status=status.HTTP_400_BAD_REQUEST)
        return Response(f'Заказ в обработке ожидайте обратного звонка! Номер заказа №{order.pk}',
                        status=status.HTTP_200_OK)


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    Продукты заказа
    Реализованы все базовые методы ModelViewSet, переделан list
    """
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def list(self, request, pk=None, *args, **kwargs):
        queryset = self.filter_queryset(OrderItem.objects.filter(order_id=pk))
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

