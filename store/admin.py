from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import (
    Product,
    Color,
    Collection,
    Order,
    OrderStatus,
    OrderItem,
    ChildrenProduct,
    Customer,
    Cart,
    CartItem
)
from cloudinary.forms import CloudinaryJsFileField


class ProductForm(forms.ModelForm):
    """
    Форма админки для продукта
    """
    description = forms.CharField(widget=CKEditorWidget(), label=Product._meta.get_field('description').verbose_name)

    class Meta:
        model = Product
        fields = '__all__'


class OrderItemInline(admin.StackedInline):
    """
    Продукты заказа
    """
    model = OrderItem
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Продукт в админке
    """
    list_display = ('id', 'name', 'vendor_code', 'collection', 'price', 'size', 'update_date', 'deleted')
    list_display_links = ('name', 'vendor_code', 'collection')
    list_filter = ('collection', 'number_in_ruler', 'size', 'material', 'start_date', 'update_date', 'end_date')
    list_editable = ('deleted',)
    readonly_fields = ('start_date', 'end_date', 'update_date', 'old_price')
    fields = ('name', 'vendor_code', 'collection', 'price', 'old_price', 'discount', 'description', 'size',
              'number_in_ruler', 'material', 'fabric_structure', 'bestseller', 'novelty', 'start_date',
              'end_date', 'update_date', 'deleted')
    search_fields = ('name', 'vendor_code', 'collection__name')
    form = ProductForm


@admin.register(ChildrenProduct)
class ChildrenProductAdmin(admin.ModelAdmin):
    """
    Подпродукт в админке
    """
    image = CloudinaryJsFileField(required=False)

    list_display = ('id', 'product', 'color', 'start_date', 'end_date', 'update_date', 'get_image', 'amount', 'deleted')
    list_display_links = ('product', 'get_image')
    list_filter = ('product', 'color', 'start_date', 'end_date', 'update_date', 'deleted')
    list_editable = ('deleted',)
    readonly_fields = ('get_image', 'start_date', 'end_date', 'update_date')
    fields = ('product', 'color', 'image', 'get_image', 'start_date', 'end_date', 'update_date', 'amount', 'deleted')
    search_fields = ('product__name', 'color__color')

    def get_image(self, obj):
        """
        Метод для получение картинки в виде отрендеренного html
        """
        return mark_safe(f'<img src={obj.image.url} width="130" height="180">') if obj.image else '-'

    get_image.short_description = 'Изображение'


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    """
    Коллекция в админке
    """
    image = CloudinaryJsFileField(required=False)

    list_display = ('id', 'name', 'start_date', 'end_date', 'update_date', 'get_image', 'deleted')
    list_display_links = ('name', 'get_image')
    list_filter = ('name', 'start_date', 'end_date', 'update_date', 'deleted')
    list_editable = ('deleted',)
    readonly_fields = ('get_image', 'start_date', 'end_date', 'update_date')
    fields = ('name', 'image', 'get_image', 'start_date', 'end_date', 'update_date', 'deleted')
    search_fields = ('name',)

    def get_image(self, obj):
        """
        Метод для получение картинки в виде отрендеренного html
        """
        return mark_safe(f'<img src={obj.image.url} width="140" height="180">') if obj.image else '-'

    get_image.short_description = 'Изображение'


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    """
    Цвета в админке
    """
    list_display = ('id', 'color', 'get_color')
    list_display_links = ('color',)
    search_fields = ('color', 'rgb')

    def get_color(self, obj):
        return mark_safe(f'<p style="color: {obj.rgb}">{obj.color}</p>')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Заказ в админке
    """
    list_display = ('id', 'first_name', 'last_name', 'get_products_count', 'get_products_sum', 'get_products_discount',
                    'get_total_price', 'start_date', 'end_date', 'update_date', 'deleted')
    list_display_links = ('id', 'first_name',)
    list_filter = ('status', 'country', 'start_date', 'end_date', 'update_date', 'deleted', 'country')
    list_editable = ('deleted',)
    readonly_fields = ('get_products_numbers_in_ruler', 'get_products_count', 'get_products_sum',
                       'get_products_discount', 'get_total_price', 'start_date', 'end_date', 'update_date')
    fields = (
        'first_name', 'last_name', 'mail', 'phone_number', 'country', 'city', 'status', 'get_products_numbers_in_ruler',
        'get_products_count', 'get_products_sum', 'get_products_discount', 'get_total_price',
        'start_date', 'end_date', 'update_date', 'deleted')
    search_fields = ('first_name', 'last_name', 'country', 'city')
    inlines = (OrderItemInline,)

    def get_products(self, obj):
        return OrderItem.objects.filter(order=obj)

    def get_products_numbers_in_ruler(self, obj):
        numbers_in_ruler = len([i for i in self.get_products(obj)])
        return numbers_in_ruler

    def get_products_count(self, obj):
        products_count = sum([i.children_product.product.number_in_ruler * i.quantity for i in self.get_products(obj)])
        return products_count

    def get_products_sum(self, obj):
        products_price = sum([i.children_product.product.price for i in self.get_products(obj)])
        return products_price

    def get_products_discount(self, obj):
        products_price = sum([
            i.children_product.product.old_price - i.children_product.product.price if i.children_product.product.old_price else 0
            for i in self.get_products(obj)])
        return products_price

    def get_total_price(self, obj):
        products_price = sum([i.total_price for i in self.get_products(obj)])
        return products_price

    get_products_numbers_in_ruler.short_description = 'Количество в линейках'
    get_products_count.short_description = 'Общее количество товаров'
    get_products_sum.short_description = 'Стоимость'
    get_products_discount.short_description = 'Скидка'
    get_total_price.short_description = 'Итог к оплате'


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)


# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ('id', 'order', 'children_product', 'get_product_price', 'quantity', 'total_price',
#                     'get_product_color', 'get_product_size', 'get_product_old_price', 'get_product_image')
#     list_display_links = ('order', 'children_product')
#     list_filter = ('order',)
#     readonly_fields = ('total_price', 'get_product_price', 'get_product_color', 'get_product_size',
#                        'get_product_old_price', 'get_product_image')
#     search_fields = ('order__first_name', 'order__last_name', 'children_product__product__name')
#     fields = ('order', 'children_product', 'get_product_price', 'quantity', 'total_price', 'get_product_color',
#               'get_product_size', 'get_product_old_price', 'get_product_image')
#
#     def get_product_price(self, obj):
#         return obj.children_product.product.price
#
#     def get_product_color(self, obj):
#         return mark_safe(f'<p style="color: {obj.children_product.color.rgb}">{obj.children_product.color.color}</p>')
#
#     def get_product_size(self, obj):
#         return obj.children_product.product.size
#
#     def get_product_old_price(self, obj):
#         return obj.children_product.product.old_price if obj.children_product.product.old_price else '-'
#
#     def get_product_image(self, obj):
#         return mark_safe(f'<img src={obj.children_product.image.url} width="140" height="180">') if obj.children_product.image else '-'
#
#     get_product_price.short_description = 'Цена'
#     get_product_color.short_description = 'Цвет'
#     get_product_size.short_description = 'Размер'
#     get_product_old_price.short_description = 'Старая цена'
#     get_product_image.short_description = 'Изображение'


class CustomerForm(forms.ModelForm):
    favorites = forms.ModelMultipleChoiceField(Product.objects.filter(deleted=False),
                                               label=Customer._meta.get_field('favorites').verbose_name)

    class Meta:
        model = Customer
        fields = '__all__'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', 'country', 'city')
    list_display_links = ('id', 'user', 'phone_number')
    form = CustomerForm


admin.site.register(CartItem)
admin.site.register(Cart)
