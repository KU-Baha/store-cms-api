from rest_framework import serializers
from .models import Product, ChildrenProduct, Collection, Color, Order, OrderStatus, OrderItem
from django.core.files.images import get_image_dimensions


class CollectionListSerializer(serializers.ModelSerializer):
    """
    Сериализатор Коллекций
    """
    class Meta:
        model = Collection
        fields = ('id', 'name', 'image')


class ChildrenProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор Подпродуктов
    """

    image = serializers.ImageField(required=False)

    def update(self, instance, validated_data):
        instance.product = validated_data.get('product', instance.product)
        instance.color = validated_data.get('color', instance.color)
        instance.image = validated_data.get('image', instance.image)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.save()
        return instance

    def validate(self, data):
        try:
            id = self.instance.id
        except AttributeError:
            id = 0
        product = data.get('product')
        color = data.get('color')
        image = data.get('image')
        try:
            # Проверка это обновление или нет
            if id == 0:
                # Валидация на максимум
                if len(ChildrenProduct.objects.filter(product=product, deleted=False)) >= 8:
                    raise serializers.ValidationError('Количество цветов не должно превышать 8ми!')
            #Валидация на цвет
            product_by_color = ChildrenProduct.objects.filter(product=product, color=color, deleted=False)
            if len(product_by_color) > 0 and product_by_color[0] != self.instance:
                raise serializers.ValidationError('Подпродукт с таким цветом уже есть!')
        except ChildrenProduct.DoesNotExist:
            raise serializers.ValidationError('Подпродукт не найден!')
        # Валидация изображения
        if image:
            width, height = get_image_dimensions(image)
            if not (1.5 <= height / width <= 1.6):
                raise serializers.ValidationError('Изображение не подходит')
        return data

    class Meta:
        model = ChildrenProduct
        fields = ('id', 'product', 'color', 'image', 'amount', 'start_date', 'update_date')


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор Продуктов
    """
    children_products = ChildrenProductSerializer(read_only=True, many=True)
    collection_name = serializers.CharField(source='collection.name', read_only=True)
    sizes = serializers.SerializerMethodField()
    old_price = serializers.IntegerField(read_only=True)

    def update(self, instance, validated_data):
        instance.collection = validated_data.get('collection', instance.collection)
        instance.name = validated_data.get('name', instance.name)
        instance.vendor_code = validated_data.get('vendor_code', instance.vendor_code)
        instance.price = validated_data.get('price', instance.price)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.description = validated_data.get('description', instance.description)
        instance.size = validated_data.get('size', instance.size)
        instance.fabric_structure = validated_data.get('fabric_structure', instance.fabric_structure)
        instance.number_in_ruler = validated_data.get('number_in_ruler', instance.number_in_ruler)
        instance.material = validated_data.get('material', instance.material)
        instance.bestseller = validated_data.get('bestseller', instance.bestseller)
        instance.novelty = validated_data.get('novelty', instance.novelty)
        instance.save()
        return instance

    def validate(self, data):
        # Валидация на формат размера
        size = data.get('size').split('-')
        if len(size) != 2 or int(size[0]) > int(size[1]):
            raise serializers.ValidationError('Формат размера не совпадает! Введите корректные данные!')
        # Валидация коллекции
        if data.get('collection').deleted:
            raise serializers.ValidationError('Коллекция была удалена! Выберите другую коллекцию')
        return data

    def get_sizes(self, obj):
        """
        Получение размеров продукта (Делает список по формату min_size до max_size)
        min_size-max_size
        """
        min_size, max_size = obj.size.split('-')
        return [x for x in range(int(min_size), int(max_size) + 1)]

    class Meta:
        model = Product
        fields = ('id', 'collection', 'collection_name', 'name', 'vendor_code', 'price', 'old_price', 'discount',
                  'description', 'size', 'sizes', 'fabric_structure', 'number_in_ruler', 'material', 'bestseller',
                  'novelty', 'children_products', 'start_date', 'update_date')