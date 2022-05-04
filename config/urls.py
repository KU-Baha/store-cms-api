"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .yasg import urlpatterns as doc_urls
from news.views import PostViewSet
from store.views import (
    ProductViewSet,
    CustomerViewSet,
    ChildrenProductViewSet,
    CollectionViewSet,
    OrderViewSet,
    CartViewSet,
    CustomerFavoriteViewSet,
)

from site_app.views import (
    QuestionAnswerViewSet,
    HelpImageViewSet,
    SliderImageViewSet,
    SiteSocialViewSet,
    CallBackViewSet,
    FooterViewSet,
    PublicOfferViewSet,
    AboutUsViewSet,
    AboutUsImageViewSet,
    OurAdvantageViewSet
)

router = DefaultRouter()

# Новости
router.register(r'news', PostViewSet, 'news')

# Магазин
router.register(r'product', ProductViewSet, 'product')
router.register(r'order', OrderViewSet, 'order')
router.register(r'customer', CustomerViewSet, 'customer')
router.register(r'children-product', ChildrenProductViewSet, 'children_product')
router.register(r'collection', CollectionViewSet, 'collection')
router.register(r'favorites', CustomerFavoriteViewSet, 'favorites')
router.register(r'cart', CartViewSet, 'cart')

# Сайт
router.register(r'question-answer', QuestionAnswerViewSet, 'question_answer')
router.register(r'help-image', HelpImageViewSet, 'help_image')
router.register(r'slider-image', SliderImageViewSet, 'slider_image')
router.register(r'social', SiteSocialViewSet, 'socials')
router.register(r'callback', CallBackViewSet, 'callback')
router.register(r'footer', FooterViewSet, 'footer')
router.register(r'public-offer', PublicOfferViewSet, 'public_offer')
router.register(r'about-us', AboutUsViewSet, 'about_us')
router.register(r'about-us-image', AboutUsImageViewSet, 'about_us_image')
router.register(r'our-advantage', OurAdvantageViewSet, 'our_advantage')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.authtoken')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
]

urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += doc_urls
