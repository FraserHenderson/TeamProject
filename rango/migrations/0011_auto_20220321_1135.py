# Generated by Django 2.2.26 on 2022-03-21 11:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0010_auto_20220321_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medium',
            name='description',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='medium',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 21, 11, 35, 25)),
        ),
    ]
