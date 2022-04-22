import json

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    ProductSerializer,
    ChildrenProductSerializer,
    CollectionSerializer,
    OrderSerializer,
    OrderItemSerializer,
    CustomerSerializer,
    UserSerializer,
    CartItemSerializer
)
from .models import (
    Product,
    ChildrenProduct,
    Collection,
    Order,
    OrderItem,
    Customer,
    Cart,
    CartItem
)

User = get_user_model()


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
    search_fields = ('name',)

    @action(methods=['get'], detail=False, url_path='similar-products/(?P<id>\d+)/(?P<qt>\d+)')
    def similar(self, request, pk=None, qt=None):
        """
        Получение похожих товаров
        """
        queryset = Product.objects.filter(collection_id=pk, deleted=False)[0:int(qt)]
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = Product.objects.get(pk=pk)
        queryset.deleted = True
        queryset.save()
        return Response('Успешно удален!', status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='bestsellers/(?P<qt>\d+)')
    def bestsellers(self, request, qt=None):
        """
        Получение товаров со статусом "Хит продаж"
        """
        queryset = self.filter_queryset(Product.objects.filter(deleted=False, bestseller=True)[0:int(qt)])
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='novelties/(?P<qt>\d+$)')
    def novelties(self, request, qt=None):
        """
        Получение товаров со статусом "Новинки"
        """
        queryset = self.filter_queryset(Product.objects.filter(deleted=False, novelty=True)[0:int(qt)])
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='search_random')
    def search_random(self, request):
        obj = []
        count = Collection.objects.all().count()
        if count >= 5:
            for i in Collection.objects.all().values_list('id')[0:5]:
                if Product.objects.order_by('?').filter(collection=i).first():
                    obj.append(Product.objects.order_by('?').filter(collection=i).first())
                else:
                    pass
        else:
            for i in Collection.objects.all().values_list('id')[0:count]:
                if Product.objects.order_by('?').filter(collection=i).first():
                    obj.append(Product.objects.order_by('?').filter(collection=i).first())
                else:
                    pass
        serializer = ProductSerializer(obj, many=True)
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
        self.paginate_queryset()
        queryset = get_object_or_404(Collection, pk=pk)
        queryset.deleted = True
        queryset.save()
        self.filter_queryset()
        return Response('Успешно удален!', status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ViewSet):
    """
    Заказ
    Реализованы все базовые методы ModelViewSet, переделан create
            Пример API для создания
        is_auntification == True:
        {
        "is_auntification": "True",
        "customer": customer_id
        }
        is_auntification == False:
        {
        "is_auntification": "False",
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
                "id": children_product_id,
                "quantity": product_quantity
                }
                ]
        }
    """

    def create(self, request, *args, **kwargs):
        json_data = request.data
        if json_data['is_auntification']:
            customer = Customer.objects.get(pk=json_data['customer'])
            order = Order.objects.create(first_name=customer.user.first_name, last_name=customer.user.last_name,
                                         mail=customer.user.email, phone_number=customer.phone_number,
                                         country=customer.country, city=customer.city)
            cart = Cart.objects.get(customer=customer)
            cart_items = CartItem.objects.filter(cart=cart)
            for cart_item in cart_items:
                if ChildrenProduct.objects.get(id=cart_item.children_product.id).amount < cart_item.quantity:
                    raise Exception('На складе меньше товаров, чем вы запросили!')
                OrderItem.objects.create(children_product_id=cart_item.children_product.id, quantity=cart_item.quantity,
                                         order=order)
                cart_item.delete()
        else:
            try:
                order = Order.objects.create(**json_data['user_data'])
                for data in json_data['products']:
                    if ChildrenProduct.objects.get(id=data['id']).amount < data['quantity']:
                        raise Exception('На складе меньше товаров, чем вы запросили!')
                    OrderItem.objects.create(children_product_id=data['id'], quantity=data['quantity'], order=order)
            except Exception as e:
                return Response(f'Ошибка при обработке заказа! Ошибка {e}', status=status.HTTP_400_BAD_REQUEST)
        return Response(f'Заказ в обработке ожидайте обратного звонка! Номер заказа №{order.pk}',
                        status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        instance = Order.objects.get(pk=pk)
        serializer = OrderSerializer(instance)
        return Response(serializer.data)

    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    @action(methods=['get'], detail=True, url_path='items')
    def items(self, request, pk=None, *args, **kwargs):
        queryset = OrderItem.objects.filter(order_id=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class CustomerViewSet(viewsets.ViewSet):
    """
    Покупатель
    """
    serializer = CustomerSerializer

    def retrieve(self, request, pk, *args, **kwargs):
        instance = Customer.objects.get(pk=pk)
        serializer = self.serializer(instance)
        user_instance = User.objects.get(id=instance.user.id)
        user_serializer = UserSerializer(user_instance)
        data = {}
        data.update(serializer.data)
        data.update(**user_serializer.data)
        return Response(data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = get_object_or_404(Customer, self.kwargs['pk'])
        serializer = self.serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class CartViewSet(viewsets.ViewSet):
    """
    Корзина
    """

    def retrieve(self, request, *args, **kwargs):
        customer = Customer.objects.get(pk=self.kwargs['pk'])
        cart = Cart.objects.get(customer=customer)
        cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    @action(methods=["post"], detail=True)
    def add_item(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        customer = Customer.objects.get(pk=self.kwargs['pk'])
        cart = Cart.objects.get(customer=customer)
        try:
            cart_item = CartItem(cart=cart, children_product_id=json_data['children_product'],
                                 quantity=json_data['quantity'])
            cart_item.save()
        except Exception as e:
            return Response(f'Ошибка: {e}', status=status.HTTP_400_BAD_REQUEST)
        return Response('Продукт добавлен в корзину!', status=status.HTTP_201_CREATED)

    @action(methods=["put"], detail=True)
    def update_item(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        customer = Customer.objects.get(pk=self.kwargs['pk'])
        cart = Cart.objects.get(customer=customer)
        cart_item = CartItem.objects.get(cart=cart, children_product=json_data['children_product'])
        cart_item.quantity = json_data['quantity']
        cart_item.save()
        return Response('Продукт в корзине обновлен!', status=status.HTTP_200_OK)

    @action(methods=["delete"], detail=True, url_path='item/(?P<children_product_id>\d+)')
    def delete_item(self, request, children_product_id, *args, **kwargs):
        customer = Customer.objects.get(pk=self.kwargs['pk'])
        cart = Cart.objects.get(customer=customer)
        cart_item = CartItem.objects.get(cart=cart, children_product=children_product_id)
        cart_item.delete()
        return Response('Продукт удален из корзины', status=status.HTTP_200_OK)
