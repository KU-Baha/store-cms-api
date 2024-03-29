# Generated by Django 4.0.3 on 2022-04-11 06:23

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUsImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Изображение странички О нас',
                'verbose_name_plural': 'Изображения странички О нас',
            },
        ),
        migrations.CreateModel(
            name='AppealType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название обращения')),
            ],
            options={
                'verbose_name': 'Тип обращения',
                'verbose_name_plural': 'Типы обращений',
            },
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=50, verbose_name='Вопрос')),
                ('answer', models.TextField(max_length=500, verbose_name='Ответ')),
            ],
            options={
                'verbose_name': 'Вопрос и ответ',
                'verbose_name_plural': 'Вопросы и ответы',
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_title', models.CharField(max_length=50, verbose_name='Заголовок сайта')),
                ('site_logo', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Логотип сайта')),
                ('about_us_title', models.CharField(default='О нас', max_length=50, verbose_name='Заголовок для "О нас"')),
                ('about_us_text', models.TextField(verbose_name='Текст для "О нас"')),
                ('footer_text', models.TextField(help_text='Слишком большой текст может поломать верстку футера, будьте осторожнее!', verbose_name='Текстовая информация в футере')),
                ('public_offer_title', models.CharField(default='Публичная оффера', max_length=50, verbose_name='Заголовок для "Публичная оффера"')),
                ('public_offer_text', models.TextField(verbose_name='Текст для "Публичная оффера"')),
                ('our_advantages_title', models.CharField(default='Наши преимущества', max_length=50, verbose_name='Заголовок для "Наши преимущества"')),
                ('our_advantages_icon', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Иконка для "Наши преимущества"')),
                ('our_advantages_text', models.TextField(verbose_name='Текст для "Наши преимущества"')),
                ('help_image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Изображение на странице "Помощь"')),
                ('start_date', models.DateTimeField(auto_now=True, verbose_name='Дата создания')),
                ('update_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата последнего изменения')),
            ],
            options={
                'verbose_name': 'Информация о магазине',
                'verbose_name_plural': 'Информация о магазине',
            },
        ),
        migrations.CreateModel(
            name='SliderImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(blank=True, help_text='Можно вместо загрузки изображние, поставить ссылку', max_length=255, null=True, verbose_name='Изображение')),
                ('link', models.CharField(blank=True, help_text='Ссылка на изображение не должно превышать 500 символов', max_length=500, null=True, verbose_name='Ссылка на изображение')),
            ],
            options={
                'verbose_name': 'Изображение слайдера',
                'verbose_name_plural': 'Изображения слайдера',
            },
        ),
        migrations.CreateModel(
            name='Social',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('icon', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Иконка')),
            ],
            options={
                'verbose_name': 'Соц сеть',
                'verbose_name_plural': 'Соц сети',
            },
        ),
        migrations.CreateModel(
            name='SiteSocial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Номер/Ник/Почта')),
                ('link', models.CharField(blank=True, help_text='Для WhatsApp генерирует автоматически', max_length=150, null=True, verbose_name='Ссылка')),
                ('social', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='site_app.social', verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Соц сеть сайта',
                'verbose_name_plural': 'Соц сети сайта',
            },
        ),
        migrations.CreateModel(
            name='CallBack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='ФИО')),
                ('number', models.CharField(max_length=15, verbose_name='Номер телефона')),
                ('create_date', models.DateTimeField(auto_now=True, verbose_name='Дата обращения')),
                ('update_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата обновления')),
                ('called', models.BooleanField(choices=[(True, 'Да'), (False, 'Нет')], default=False, verbose_name='Позвонили?')),
                ('appeal_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='site_app.appealtype', verbose_name='Тип обращения')),
            ],
            options={
                'verbose_name': 'Обратный звонок',
                'verbose_name_plural': 'Обратные звонки',
            },
        ),
    ]
