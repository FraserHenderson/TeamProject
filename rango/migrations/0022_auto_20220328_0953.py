# Generated by Django 2.2.26 on 2022-03-28 09:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0021_merge_20220328_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medium',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 28, 9, 53, 12)),
        ),
        migrations.AlterField(
            model_name='review',
            name='upload_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 28, 9, 53, 12)),
        ),
    ]
