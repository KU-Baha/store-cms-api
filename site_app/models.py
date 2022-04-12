from django.core.exceptions import ValidationError
from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings


class Site(models.Model):
    """
    Информация о магазине.
    Сохранить больше двух моделей нельзя!
    """
    site_title = models.CharField('Заголовок сайта', max_length=50)
    site_logo = CloudinaryField('Логотип сайта')
    # Хедер
    header_phone = models.CharField('Номер телефона в хедере', max_length=50)
    # О нас
    about_us_title = models.CharField('Заголовок для "О нас"', max_length=50, default='О нас')
    about_us_text = models.TextField('Текст для "О нас"')
    # Футер
    footer_text = models.TextField('Текстовая информация в футере', help_text='Слишком большой текст может поломать '
                                                                              'верстку футера, будьте осторожнее!')
    # Публичная оффера
    public_offer_title = models.CharField('Заголовок для "Публичная оффера"', max_length=50, default='Публичная оффера')
    public_offer_text = models.TextField('Текст для "Публичная оффера"')
    # Помощь
    help_image = CloudinaryField('Изображение на странице "Помощь"')

    start_date = models.DateTimeField('Дата создания', auto_now=True)
    update_date = models.DateTimeField('Дата последнего изменения', auto_now_add=True)

    def __str__(self):
        return self.site_title

    def save(self, *args, **kwargs):
        if self._state.adding:
            if len(Site.objects.all()) > 0:
                pass
            else:
                super().save(*args, **kwargs)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Информация о магазине'
        verbose_name_plural = 'Информация о магазине'


class SiteSocial(models.Model):
    """
    Соц-сети/Номера телефонов/Почта --- Сайта
    """
    social = models.ForeignKey('Social', on_delete=models.DO_NOTHING, verbose_name='Тип')
    name = models.CharField('Номер/Ник/Почта', max_length=50)
    link = models.CharField('Ссылка', max_length=150, null=True, blank=True,
                            help_text='Для WhatsApp генерирует автоматически')

    def save(self, *args, **kwargs):
        if self.social.name == settings.CHOICES_SOCIALS[0][0]:
            self.link = f'https://wa.me/{self.name}'
        elif self.social.name == settings.CHOICES_SOCIALS[1][0]:
            self.link = f'https://www.instagram.com/{self.name}/'
        elif self.social.name == settings.CHOICES_SOCIALS[2][0]:
            self.link = f'https://t.me/{self.name}/'
        elif self.social.name == settings.CHOICES_SOCIALS[3][0]:
            self.link = f'{self.name}'
        elif self.social.name == settings.CHOICES_SOCIALS[4][0]:
            self.link = f'tel:{self.name}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Соц сеть сайта'
        verbose_name_plural = 'Соц сети сайта'


class Social(models.Model):
    """
    Название - Соц-сети
    """
    name = models.CharField('Название', max_length=50, choices=settings.CHOICES_SOCIALS)
    icon = CloudinaryField('Иконка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Соц сеть'
        verbose_name_plural = 'Соц сети'


class SliderImage(models.Model):
    """
    Изображения слайдера
    """
    image = CloudinaryField('Изображение', help_text='Можно вместо загрузки изображние, поставить ссылку', null=True, blank=True)
    link = models.CharField('Ссылка на изображение', max_length=500,  null=True, blank=True,
                            help_text='Ссылка на изображение не должно превышать 500 символов')

    def __str__(self):
        if self.image:
            return str(self.image)
        else:
            return self.link

    class Meta:
        verbose_name = 'Изображение слайдера'
        verbose_name_plural = 'Изображения слайдера'


class QuestionAnswer(models.Model):
    """
    Старничка помощь вопрос и ответ
    """
    question = models.CharField('Вопрос', max_length=50)
    answer = models.TextField('Ответ', max_length=500)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос и ответ'
        verbose_name_plural = 'Вопросы и ответы'


class CallBack(models.Model):
    """
    Обратный звонок
    """
    name = models.CharField('ФИО', max_length=50)
    number = models.CharField('Номер телефона', max_length=15)
    appeal_type = models.ForeignKey('AppealType', on_delete=models.DO_NOTHING, verbose_name='Тип обращения')
    create_date = models.DateTimeField('Дата обращения', auto_now=True)
    update_date = models.DateTimeField('Дата обновления', auto_now_add=True)
    called = models.BooleanField('Позвонили?', default=False, choices=((True, 'Да'), (False, 'Нет')))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Обратный звонок'
        verbose_name_plural = 'Обратные звонки'


class AppealType(models.Model):
    """
    Тип обращения
    """
    name = models.CharField('Название обращения', max_length=30, choices=settings.CHOICES_APPEAL_TYPES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип обращения'
        verbose_name_plural = 'Типы обращений'


class AboutUsImage(models.Model):
    """
    Изображение странички О нас
    """
    image = CloudinaryField('Изображение')

    def __str__(self):
        return self.image.url

    class Meta:
        verbose_name = 'Изображение странички О нас'
        verbose_name_plural = 'Изображения странички О нас'


class OurAdvantages(models.Model):
    title = models.CharField('Заголовок', max_length=50, default='Наши преимущества')
    icon = CloudinaryField('Иконка')
    text = models.TextField('Текст')

    class Meta:
        verbose_name = 'Наши преимущества'
        verbose_name_plural = 'Наши преимущества'