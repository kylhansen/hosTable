# Generated by Django 2.1.7 on 2019-03-05 22:27

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('users', '0005_auto_20190305_2222'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaggedRestriction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField(db_index=True, verbose_name='Object id')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_taggedrestriction_tagged_items', to='contenttypes.ContentType', verbose_name='Content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_TaggedRestrictions_items', to='users.RestrictionTags')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='taggedrestrictions',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='taggedrestrictions',
            name='tag',
        ),
        migrations.AlterField(
            model_name='profile',
            name='restrictions',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='users.TaggedRestriction', to='users.RestrictionTags', verbose_name='Tags'),
        ),
        migrations.DeleteModel(
            name='TaggedRestrictions',
        ),
    ]
