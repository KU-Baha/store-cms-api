# Generated by Django 4.0.3 on 2022-04-06 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='total_price',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Общая цена'),
        ),
    ]
