from django import forms
from django.contrib import admin

from ckeditor.widgets import CKEditorWidget
from django.utils.safestring import mark_safe

from .models import Site, SiteSocial, Social, SliderImage, QuestionAnswer, CallBack, AppealType, AboutUsImage


class SiteForm(forms.ModelForm):
    """
    Форма для админ панели "Информация сайта"
    """
    about_us_text = forms.CharField(widget=CKEditorWidget(), label=Site._meta.get_field('about_us_text').verbose_name)
    footer_text = forms.CharField(widget=CKEditorWidget(), label=Site._meta.get_field('footer_text').verbose_name)
    public_offer_text = forms.CharField(widget=CKEditorWidget(), label=Site._meta.get_field('public_offer_text').verbose_name)
    our_advantages_text = forms.CharField(widget=CKEditorWidget(), label=Site._meta.get_field('our_advantages_text').verbose_name)

    class Meta:
        model = Site
        fields = '__all__'


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    """
    Админ панель "Информация сайта"
    """
    form = SiteForm
    list_display = ('site_title', 'get_site_logo')
    list_display_links = ('site_title', 'get_site_logo')
    readonly_fields = ('get_site_logo',)

    def get_site_logo(self, obj):
        return mark_safe(f"<img src={obj.site_logo.url}>")

    get_site_logo.short_description = 'Логотип'


@admin.register(SiteSocial)
class SiteSocialAdmin(admin.ModelAdmin):
    """
    Админ панель "Соц сети сайта"
    """
    list_display = ('id', 'social', 'name', 'link')
    list_display_links = ('social', 'name')
    list_filter = ('social', 'name')


@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    """
    Админ панель "Соц сети"
    """
    list_display = ('name', 'get_icon')

    def get_icon(self, obj):
        if obj.icon:
            return mark_safe(f'<img src={obj.icon.url} width=50 height=50>')
        return mark_safe("-")

    get_icon.short_description = 'Иконка'


@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    """
    Админ панель "Изображения слайдера"
    """
    list_display = ('id', 'get_image')
    list_display_links = ('id', 'get_image')
    readonly_fields = ('get_image', )
    ordering = ('id', )

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="250" height="120">')
        else:
            return mark_safe(f'<img src={obj.link} width="50" height="60">')

    get_image.short_description = 'Изображение'


@admin.register(CallBack)
class CallBackAdmin(admin.ModelAdmin):
    """
    Админ панель "Обратные звонки"
    """
    list_display = ('id', 'name', 'number', 'create_date', 'appeal_type', 'called')
    list_display_links = ('id', 'name')
    list_editable = ('called',)
    list_filter = ('appeal_type', 'called', 'create_date', 'update_date')


@admin.register(AboutUsImage)
class AboutUsImageAdmin(admin.ModelAdmin):
    """
    Админ панель "Изображения странички о нас"
    """
    list_display = ('get_image',)
    list_display_links = ('get_image',)
    readonly_fields = ('get_image', )
    ordering = ('id', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = 'Изображение'


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    """
    Админ панель "Вопросы и ответы"
    """
    list_display = ('question', 'answer')
    list_display_links = ('question', )


@admin.register(AppealType)
class AppealTypeAdmin(admin.ModelAdmin):
    """
    Админ панель "Тип обращения"
    """
    list_display = ('name', )
    list_display_links = ('name', )
    ordering = ('id', )

