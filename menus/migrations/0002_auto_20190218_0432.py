# Generated by Django 2.1.5 on 2019-02-18 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='recipe',
            new_name='recipe_link',
        ),
    ]