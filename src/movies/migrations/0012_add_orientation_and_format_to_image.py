# Generated by Django 3.1.5 on 2021-03-23 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0011_delete_actor_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='poster',
            name='format',
            field=models.CharField(choices=[('LARGE', 'Большой'), ('MEDIUM', 'Средний'), ('SMALL', 'Маленький')], default='MEDIUM', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='poster',
            name='orientation',
            field=models.CharField(choices=[('VERTICAL', 'Вертикальный'), ('HORIZONTAL', 'Горизонтальный')], default='VERTICAL', max_length=10),
            preserve_default=False,
        ),
    ]
