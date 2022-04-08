from django.core.validators import MinValueValidator
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from colorful.fields import RGBColorField
from datetime import datetime, timezone
from cloudinary.models import CloudinaryField


class Product(models.Model):
    """
    Модель продукта
    Связь с Collection
    """
    name = models.CharField('Название', max_length=50)
    vendor_code = models.CharField('Артикл', max_length=50)
    price = models.PositiveIntegerField('Цена')
    old_price = models.PositiveIntegerField('Старая цена', null=True, blank=True)
    discount = models.PositiveSmallIntegerField('Скидка в процентах', null=True, blank=True)
    description = models.TextField('Описание', max_length=1500)
    size = models.CharField('Размерный ряд', max_length=50, help_text="Формат строго: n-n. Пример 42-50")
    fabric_structure = models.CharField('Состав ткани', max_length=50)
    number_in_ruler = models.PositiveSmallIntegerField('Количество в линейке', default=0)
    material = models.CharField('Материал', max_length=20)
    collection = models.ForeignKey('Collection', on_delete=models.DO_NOTHING, null=True, blank=True,
                                   verbose_name='Коллекция', related_name='products')
    bestseller = models.BooleanField('Хит продаж', default=False)
    novelty = models.BooleanField('Новинка', default=True)
    start_date = models.DateTimeField('Дата создания', auto_now=True)
    end_date = models.DateTimeField('Дата удаления', null=True, blank=True)
    update_date = models.DateTimeField('Дата последнего изменения', auto_now_add=True)
    deleted = models.BooleanField('Удален?', default=False, choices=settings.CHOICES_YES_NO)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Проверка на удаление
        if self.deleted:
            self.end_date = datetime.now(tz=timezone.utc)
        else:
            self.end_date = None
        # Подсчет скидки
        if self.discount:
            self.old_price = self.price
            self.price = self.price - (self.price / 100 * self.discount)
        super().save(*args, **kwargs)

    def clean(self):
        # Валидация на формат размера
        data = self.size.split('-')
        if len(data) != 2 or int(data[0]) > int(data[1]):
            raise ValidationError('Формат размера не совпадает! Введите корректные данные!')
        # Валидация коллекции
        try:
            if self.collection.deleted:
                raise ValidationError('Коллекция была удалена! Выберите другую коллекцию')
        except Collection.DoesNotExist:
            raise ValidationError('Коллекция не найдена! Выберите другую коллекцию')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['deleted', 'id']


class ChildrenProduct(models.Model):
    """
    Модель Подпродукта
    Связь с Product и Color
    Внешняя связь с OrderItem
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='children_products')
    color = models.ForeignKey('Color', on_delete=models.DO_NOTHING, verbose_name='Цвет', related_name='children_products')
    image = CloudinaryField('Изображение')
    amount = models.PositiveSmallIntegerField('Количество на складе', default=0)
    start_date = models.DateTimeField('Дата создания', auto_now=True)
    end_date = models.DateTimeField('Дата удаления', null=True, blank=True)
    update_date = models.DateTimeField('Дата последнего изменения', auto_now_add=True)
    deleted = models.BooleanField('Удален?', default=False, choices=settings.CHOICES_YES_NO)

    def save(self, *args, **kwargs):
        # Проверка на удаление
        if self.deleted:
            self.end_date = datetime.now(tz=timezone.utc)
        else:
            self.end_date = None
        super().save(*args, **kwargs)

    def clean(self):
        try:
            # Проверка это обновление или нет
            if not ChildrenProduct.objects.get(pk=self.pk):
                # Валидация на максимум
                if len(ChildrenProduct.objects.filter(product=self.product, deleted=False)) >= 8:
                    raise ValidationError('Количество цветов не должно превышать 8ми!')
            # Валидация на цвет
            product_by_color = ChildrenProduct.objects.filter(product=self.product, color_id=self.color.pk, deleted=False)
            if len(product_by_color) > 0 and product_by_color[0] != self:
                raise ValidationError('Подпродукт с таким цветом уже есть!')
        except ChildrenProduct.DoesNotExist:
            raise ValidationError('Подпродукт не найден!')
        # Валидация изображения
        if self.image:
            try:
                width, height = get_image_dimensions(self.image)
                if not (1.5 <= height / width <= 1.6):
                    raise ValidationError('Изображение не подходит')
            except TypeError:
                pass

    def __str__(self):
        return f'{self.product} - {self.color}: {self.amount}'

    class Meta:
        verbose_name = 'Подпродукт'
        verbose_name_plural = 'Подпродукты'


class Collection(models.Model):
    """
    Модель коллекций
    Внешние связи: Product
    """
    name = models.CharField('Название', max_length=50)
    image = CloudinaryField('Изображение', blank=False)
    start_date = models.DateTimeField('Дата создания', auto_now=True)
    end_date = models.DateTimeField('Дата удаления', null=True, blank=True)
    update_date = models.DateTimeField('Дата последнего изменения', auto_now_add=True)
    deleted = models.BooleanField('Удален?', default=False, choices=settings.CHOICES_YES_NO)

    def save(self, *args, **kwargs):
        # Проверка на удаление
        if self.deleted:
            self.end_date = datetime.now(tz=timezone.utc)
        else:
            self.end_date = None
        super().save(*args, **kwargs)

    def clean(self):
        # Валидация изображение
        if self.image:
            try:
                width, height = get_image_dimensions(self.image)
                if not (1.11 <= height / width <= 1.19):
                    raise ValidationError('Изображение не подходит')
            except TypeError:
                pass

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'
        ordering = ['id']


class Color(models.Model):
    """
    Модель цветов для продукта
    Внешняя связь с ChildrenProduct
    """
    color = models.CharField('Название', max_length=50)
    rgb = RGBColorField()

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


class Order(models.Model):
    """
    Модель заказа
    Связь с OrderStatus
    Внешняя связь с OrderItem
    """
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    mail = models.EmailField('Электронная почта', null=True, blank=True)
    phone_number = models.CharField('Телефонный номер', max_length=20)
    country = models.CharField('Страна', max_length=50)
    city = models.CharField('Город', max_length=50)
    issue_date = models.DateTimeField('Дата оформления', auto_now=True)
    status = models.ForeignKey('OrderStatus', on_delete=models.DO_NOTHING, verbose_name='Статус заказа', default=1)
    start_date = models.DateTimeField('Дата создания', auto_now=True)
    end_date = models.DateTimeField('Дата удаления', null=True, blank=True)
    update_date = models.DateTimeField('Дата последнего изменения', auto_now_add=True)
    deleted = models.BooleanField('Удален?', default=False, choices=settings.CHOICES_YES_NO)

    def save(self, *args, **kwargs):
        # Проверка на удаление
        if self.deleted:
            self.end_date = datetime.now(tz=timezone.utc)
        else:
            self.end_date = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.last_name} - {self.first_name}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderStatus(models.Model):
    """
    Модель статус заказа
    Внешняя связь с Order
    """
    name = models.CharField('Статус заказа', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'


class OrderItem(models.Model):
    """
    Модель продукт заказа
    Связь с Order и ChildrenProduct
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    children_product = models.ForeignKey(ChildrenProduct, related_name='order_items', on_delete=models.DO_NOTHING, verbose_name='Продукт')
    quantity = models.PositiveIntegerField('Количество', default=1, validators=[MinValueValidator(1)])
    total_price = models.PositiveIntegerField('Общая цена', null=True, blank=True)

    def save(self, *args, **kwargs):
        product = ChildrenProduct.objects.get(pk=self.children_product.pk)
        product.amount -= self.quantity
        product.save()
        self.total_price = product.product.price * self.quantity
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        product = ChildrenProduct.objects.get(pk=self.children_product.pk)
        product.amount += self.quantity
        product.save()
        super(OrderItem, self).delete()

    def clean(self):
        if not self._state.adding:
            raise ValidationError('Обновление запрещено!')
        if self.children_product.amount < self.quantity:
            raise ValidationError('На складе меньше товаров, чем вы запросили!')

    def __str__(self):
        return f'{self.order} - {self.children_product}'

    class Meta:
        verbose_name = 'Продукт заказа'
        verbose_name_plural = 'Продукты заказов'
