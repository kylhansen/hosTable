# Generated by Django 2.1.7 on 2019-03-05 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0011_auto_20190304_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='foods',
            field=models.ManyToManyField(blank=True, to='menus.Food'),
        ),
    ]