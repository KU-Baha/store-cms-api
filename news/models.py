from django.db import models
from datetime import datetime, timezone


class Post(models.Model):
    image = models.ImageField('Изображение')
    title = models.CharField('Заголовок', max_length=50)
    description = models.TextField('Описание', max_length=1500)
    create_date = models.DateTimeField('Дата создания', auto_now=True)
    end_date = models.DateTimeField('Дата удаления', null=True, blank=True)
    update_date = models.DateTimeField('Дата обновления', auto_now_add=True)
    is_active = models.BooleanField('Активен?', default=True, choices=((True, 'Да'), (False, 'Нет')))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Проверка на удаление
        if self.is_active and self.end_date:
            self.end_date = None
        else:
            self.end_date = datetime.now(tz=timezone.utc)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'