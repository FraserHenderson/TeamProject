# Generated by Django 2.2.26 on 2022-03-25 15:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0016_auto_20220325_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medium',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 25, 15, 55, 1)),
        ),
        migrations.AlterField(
            model_name='medium',
            name='thumbnail',
            field=models.ImageField(default='Default_profile_picture.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='review',
            name='upload_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 25, 15, 55, 1)),
        ),
    ]
