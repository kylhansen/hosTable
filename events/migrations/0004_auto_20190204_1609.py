# Generated by Django 2.1.5 on 2019-02-04 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_remove_event_event_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='RSVP_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(),
        ),
    ]
