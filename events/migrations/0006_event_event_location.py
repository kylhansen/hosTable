# Generated by Django 2.1.5 on 2019-02-04 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20190204_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_location',
            field=models.CharField(blank=True, default='TBD', max_length=100, null=True),
        ),
    ]
