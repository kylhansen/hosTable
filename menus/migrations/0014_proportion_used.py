# Generated by Django 2.1.7 on 2019-04-18 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0013_auto_20190306_0553'),
    ]

    operations = [
        migrations.AddField(
            model_name='proportion',
            name='used',
            field=models.FloatField(default=0.0),
        ),
    ]
