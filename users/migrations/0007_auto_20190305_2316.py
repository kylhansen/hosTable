# Generated by Django 2.1.7 on 2019-03-05 23:16

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20190305_2227'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestrictionTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Restriction Tag',
                'verbose_name_plural': 'Restriction Tags',
            },
        ),
        migrations.AddField(
            model_name='taggedrestriction',
            name='sensetivity',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='profile',
            name='restrictions',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='users.TaggedRestriction', to='users.RestrictionTag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='taggedrestriction',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_TaggedRestrictions_items', to='users.RestrictionTag'),
        ),
        migrations.DeleteModel(
            name='RestrictionTags',
        ),
    ]
