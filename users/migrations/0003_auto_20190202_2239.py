# Generated by Django 2.1.5 on 2019-02-02 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190202_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='first',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last',
            field=models.CharField(default='', max_length=100),
        ),
    ]
