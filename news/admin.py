from cloudinary.forms import CloudinaryJsFileField
from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from .models import Post
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    """
    Форма поста
    """
    description = forms.CharField(widget=CKEditorWidget(), label=Post._meta.get_field('description').verbose_name)

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Пост в админке
    """
    list_display = ('id', 'title', 'create_date', 'end_date', 'update_date', 'get_image', 'deleted')
    list_display_links = ('id', 'title', 'get_image')
    list_editable = ('deleted',)
    list_filter = ('create_date', 'end_date', 'update_date', 'deleted')
    readonly_fields = ('create_date', 'end_date', 'update_date', 'get_image')
    search_fields = ('title', )
    form = PostForm
    fields = ('title', 'description', 'create_date', 'end_date', 'update_date', 'image', 'get_image', 'deleted')

    def get_image(self, obj):
        """
        Метод для получение картинки в виде отрендеренного html
        """
        return mark_safe(f'<img src={obj.image.url} width="140" height="180">') if obj.image else '-'

    get_image.short_description = 'Изображение'