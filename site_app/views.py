from rest_framework import viewsets
from rest_framework.decorators import action
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


class HelpImageViewSet(viewsets.ViewSet):
    """
    Изображение на страничке 'Помощь'
    """
    serializer_class = HelpImageSerializer
    queryset = Site.objects.first()

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset)
        return Response(serializer.data)

    @action(methods=["put"], detail=False, url_path='update')
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.serializer_class(self.queryset, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
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


class FooterViewSet(viewsets.ViewSet):
    """
    Футер
    """
    serializer_class = FooterSerializer
    queryset = Site.objects.first()

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset)
        return Response(serializer.data)

    @action(methods=["put"], detail=False, url_path='update')
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.serializer_class(self.queryset, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class PublicOfferViewSet(viewsets.ViewSet):
    """
    Публичная офера
    """
    serializer_class = PublicOfferSerializer
    queryset = Site.objects.first()

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset)
        return Response(serializer.data)

    @action(methods=["put"], detail=False, url_path='update')
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.serializer_class(self.queryset, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class AboutUsViewSet(viewsets.ViewSet):
    """
    О нас
    """
    serializer_class = AboutUsSerializer
    queryset = Site.objects.first()

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset)
        img_queryset = AboutUsImage.objects.all()
        img_serializer = AboutUsImageSerializer(img_queryset, many=True)
        return Response({'data': serializer.data, 'about_images': img_serializer.data})

    @action(methods=["put"], detail=False, url_path='update')
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = self.serializer_class(self.queryset, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
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
