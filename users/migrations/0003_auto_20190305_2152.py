# Generated by Django 2.1.7 on 2019-03-05 21:52

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('users', '0002_profile_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllergyTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
                ('sensetivity', models.IntegerField(default=5)),
            ],
            options={
                'verbose_name': 'Allergy Tag',
                'verbose_name_plural': 'Allergy Tags',
            },
        ),
        migrations.CreateModel(
            name='TaggedAllergies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField(db_index=True, verbose_name='Object id')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_taggedallergies_tagged_items', to='contenttypes.ContentType', verbose_name='Content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_TaggedAllergies_items', to='users.AllergyTags')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='users.TaggedAllergies', to='users.AllergyTags', verbose_name='Tags'),
        ),
    ]
