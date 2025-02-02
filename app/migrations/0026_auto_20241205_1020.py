# Generated by Django 2.2.28 on 2024-12-05 07:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20241205_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2024, 12, 5, 10, 20, 15, 7971), verbose_name='Опубликована'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2024, 12, 5, 10, 20, 15, 8968), verbose_name='Дата комментария'),
        ),
    ]
