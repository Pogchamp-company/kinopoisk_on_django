# Generated by Django 3.1.5 on 2021-03-22 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_add_person_photo_rel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='composers',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='directors',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='editors',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='operators',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='producers',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='production_designers',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='writers',
        ),
    ]
