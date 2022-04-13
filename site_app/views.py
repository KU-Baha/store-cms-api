from rest_framework import viewsets
from rest_framework.response import Response

from .models import (
    Site,
    QuestionAnswer,
    SliderImage,
    SiteSocial,
    CallBack,
    AboutUsImage,
    OurAdvantages
)

from .serializers import (
    QuestionAnswerSerializer,
    SliderImageSerializer,
    SiteSocialSerializer,
    CallBackSerializer,
    FooterSerializer,
    PublicOfferSerializer,
    AboutUsSerializer,
    AboutUsImageSerializer,
    HelpImageSerializer,
    OurAdvantageSerializer
)


class QuestionAnswerViewSet(viewsets.ModelViewSet):
    """
    Вопросы и ответы
    """
    serializer_class = QuestionAnswerSerializer
    queryset = QuestionAnswer.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        img_serializer = HelpImageSerializer(Site.objects.first())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'data': serializer.data, 'image': img_serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data, 'image': img_serializer.data})


class HelpImageViewSet(viewsets.ModelViewSet):
    """
    Изображение на страничке 'Помощь'
    """
    serializer_class = HelpImageSerializer
    queryset = Site.objects.first()

    def retrieve(self, request, *args, **kwargs):
        instance = self.queryset
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.queryset
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class SliderImageViewSet(viewsets.ModelViewSet):
    """
    Изображения слайдера
    """
    serializer_class = SliderImageSerializer
    queryset = SliderImage.objects.all()


class SiteSocialViewSet(viewsets.ModelViewSet):
    """
    Соц сети сайта
    """
    serializer_class = SiteSocialSerializer
    queryset = SiteSocial.objects.all()


class CallBackViewSet(viewsets.ModelViewSet):
    """
    Обратная связь
    """
    serializer_class = CallBackSerializer
    queryset = CallBack.objects.all()


class FooterViewSet(viewsets.ModelViewSet):
    """
    Футер
    """
    serializer_class = FooterSerializer
    queryset = Site.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = Site.objects.first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = Site.objects.first()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # Если 'prefetch_related' был применен к набору запросов, нам нужно
            # принудительно аннулировать кеш предварительной выборки экземпляра.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class PublicOfferViewSet(viewsets.ModelViewSet):
    """
    Публичная офера
    """
    serializer_class = PublicOfferSerializer
    queryset = Site.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = Site.objects.first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = Site.objects.first()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # Если 'prefetch_related' был применен к набору запросов, нам нужно
            # принудительно аннулировать кеш предварительной выборки экземпляра.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class AboutUsViewSet(viewsets.ModelViewSet):
    """
    О нас
    """
    serializer_class = AboutUsSerializer
    queryset = Site.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = Site.objects.first()
        serializer = self.get_serializer(instance)
        img_queryset = AboutUsImage.objects.all()
        img_serializer = AboutUsImageSerializer(img_queryset, many=True)
        return Response({'data': serializer.data, 'about_images': img_serializer.data})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = Site.objects.first()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # Если 'prefetch_related' был применен к набору запросов, нам нужно
            # принудительно аннулировать кеш предварительной выборки экземпляра.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class AboutUsImageViewSet(viewsets.ModelViewSet):
    """
    Изображения 'О нас'
    """
    serializer_class = AboutUsImageSerializer
    queryset = AboutUsImage.objects.all()


class OurAdvantageViewSet(viewsets.ModelViewSet):
    """
    Наши преймущества
    """
    serializer_class = OurAdvantageSerializer
    queryset = OurAdvantages.objects.all()
