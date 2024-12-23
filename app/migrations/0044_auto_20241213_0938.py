# Generated by Django 2.2.28 on 2024-12-13 06:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_auto_20241213_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2024, 12, 13, 9, 38, 11, 825303), verbose_name='Опубликована'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2024, 12, 13, 9, 38, 11, 826800), verbose_name='Дата комментария'),
        ),
    ]
