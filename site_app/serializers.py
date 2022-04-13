from rest_framework import serializers
from django.conf import settings

from .models import (
    Site,
    SiteSocial,
    SliderImage,
    QuestionAnswer,
    CallBack,
    AboutUsImage,
    OurAdvantages
)


class QuestionAnswerSerializer(serializers.ModelSerializer):
    """
    Вопросы и ответы
    """
    class Meta:
        model = QuestionAnswer
        fields = ('question', 'answer')


class HelpImageSerializer(serializers.ModelSerializer):
    """
    Изображение помощи
    """
    help_image = serializers.ImageField(required=False)

    class Meta:
        model = Site
        fields = ('help_image',)


class PublicOfferSerializer(serializers.ModelSerializer):
    """
    Публичная оффера
    """

    class Meta:
        model = Site
        fields = ('public_offer_title', 'public_offer_text')


class SiteSocialSerializer(serializers.ModelSerializer):
    """
    Создание Соц-сети/Номера телефонов/Почта --- Сайта
    """

    class Meta:
        model = SiteSocial
        fields = ('social', 'name', 'link')


class FooterSerializer(serializers.ModelSerializer):
    """
    Футер
    """
    social = SiteSocialSerializer(read_only=True, many=True)
    site_logo = serializers.ImageField(required=False)

    class Meta:
        model = Site
        fields = ('site_logo', 'footer_text', 'social')


class AboutUsImageSerializer(serializers.ModelSerializer):
    """
    Изображения для странички О нас
    """

    image = serializers.ImageField(required=False)

    class Meta:
        model = AboutUsImage
        fields = ('image', )


class AboutUsSerializer(serializers.ModelSerializer):
    """
    О Нас
    """
    class Meta:
        model = Site
        fields = ('about_us_title', 'about_us_text')


class CallBackSerializer(serializers.ModelSerializer):
    """
    Обратный звонок
    """
    appeal_type_name = serializers.CharField(source='appeal_type.name', read_only=True)

    class Meta:
        model = CallBack
        fields = ('name', 'number', 'appeal_type_name', 'appeal_type')


class SliderImageSerializer(serializers.ModelSerializer):
    """
    Изображения слайдера
    """
    image = serializers.ImageField(required=False)

    class Meta:
        model = SliderImage
        fields = ('image', 'link')


class OurAdvantageSerializer(serializers.ModelSerializer):
    """
    Наши преймущества
    """
    icon = serializers.ImageField(required=False)

    class Meta:
        model = OurAdvantages
        fields = ('title', 'icon', 'text')