from django.urls import path
from .views import (
    QuestionAnswerViewSet,
    SliderImageViewSet,
    SiteSocialViewSet,
    CallBackViewSet,
    FooterViewSet,
    PublicOfferViewSet,
    AboutUsViewSet,
    AboutUsImageViewSet,
    HelpImageViewSet,
    OurAdvantageViewSet
)

urlpatterns = [
    path('questions-answers/', QuestionAnswerViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('question-answer/<int:pk>/', QuestionAnswerViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                                     'patch': 'partial_update', 'delete': 'destroy'})),
    path('question-answer/image/', HelpImageViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                             'patch': 'partial_update'})),
    path('sliders/', SliderImageViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('slider/<int:pk>/', SliderImageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update',
                                                         'delete': 'destroy'})),
    path('socials-site/', SiteSocialViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('social-site/<int:pk>/', SiteSocialViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                             'patch': 'partial_update', 'delete': 'destroy'})),
    path('callbacks/', CallBackViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('callback/<int:pk>/', CallBackViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                        'patch': 'partial_update', 'delete': 'destroy'})),
    path('footer/', FooterViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'})),
    path('public_offer/', PublicOfferViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'})),
    path('about/', AboutUsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'})),
    path('about/images/', AboutUsImageViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('about/image/<int:pk>/', AboutUsImageViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                               'patch': 'partial_update'})),
    path('our-advantage/', OurAdvantageViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('our-advantage/<int:pk>/',
         OurAdvantageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}))
]
