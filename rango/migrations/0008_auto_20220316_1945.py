# Generated by Django 2.2.26 on 2022-03-16 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0007_auto_20220316_1748'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medium',
            old_name='medium_category',
            new_name='medium_categories',
        ),
    ]
