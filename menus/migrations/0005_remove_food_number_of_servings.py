# Generated by Django 2.1.5 on 2019-02-18 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0004_auto_20190218_0445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='number_of_servings',
        ),
    ]
