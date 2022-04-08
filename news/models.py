from django.db import models
from django.conf import settings
from datetime import datetime, timezone
from cloudinary.models import CloudinaryField


class Post(models.Model):
    title = models.CharField('Заголовок', max_length=50)
    description = models.TextField('Описание', max_length=1500)
    image = CloudinaryField('Изображение')
    create_date = models.DateTimeField('Дата создания', auto_now=True)
    end_date = models.DateTimeField('Дата удаления', null=True, blank=True)
    update_date = models.DateTimeField('Дата обновления', auto_now_add=True)
    deleted = models.BooleanField('Удален?', default=False, choices=settings.CHOICES_YES_NO)

    def save(self, *args, **kwargs):
        # Проверка на удаление
        if self.deleted:
            self.end_date = datetime.now(tz=timezone.utc)
        else:
            self.end_date = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'