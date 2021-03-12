# Generated by Django 3.1.5 on 2021-03-07 07:45

from django.db import migrations, models
import django.db.models.deletion
import django_minio_backend.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=100)),
                ('birth_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(storage=django_minio_backend.models.MinioBackend(bucket_name='images'), upload_to=django_minio_backend.models.iso_date_prefix)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='person.person')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]