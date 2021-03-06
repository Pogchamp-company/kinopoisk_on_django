# Generated by Django 3.1.5 on 2021-05-05 16:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_minio_backend.models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0014_add_movie_trailers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='movie',
            options={'verbose_name': 'Фильм', 'verbose_name_plural': 'Фильмы'},
        ),
        migrations.AlterModelOptions(
            name='movietrailer',
            options={'verbose_name': 'Трейлер', 'verbose_name_plural': 'Трейлеры'},
        ),
        migrations.AlterModelOptions(
            name='movietype',
            options={'verbose_name': 'Тип Фильма', 'verbose_name_plural': 'Типы фильмов'},
        ),
        migrations.AlterModelOptions(
            name='poster',
            options={'verbose_name': 'Постер', 'verbose_name_plural': 'Постеры'},
        ),
        migrations.AddField(
            model_name='score',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.RunSQL('''UPDATE movies_score SET created_at = NOW() - interval '13 hours' '''),
        migrations.AlterField(
            model_name='score',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),

        migrations.AlterField(
            model_name='genre',
            name='title',
            field=models.CharField(max_length=30, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='age_rating',
            field=models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxLengthValidator(18)], verbose_name='Возрастное ограничение'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='budget',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Бюджет'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.TextField(null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='duration',
            field=models.DurationField(verbose_name='Продолжительность'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(related_name='movies', to='movies.Genre', verbose_name='Жанры'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='movie_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='movies', to='movies.movietype', verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='original_title',
            field=models.CharField(max_length=150, verbose_name='Оригинальное название'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='premiere',
            field=models.DateField(null=True, verbose_name='Премьера (мир)'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='premiere_ru',
            field=models.DateField(null=True, verbose_name='Премьера (Россия)'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='rating_mpaa',
            field=models.CharField(choices=[('G', 'G'), ('PG', 'PG'), ('PG_13', 'PG-13'), ('R', 'R'), ('NC_17', 'NC-17')], max_length=5, null=True, verbose_name='Рейтинг MPAA'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='slogan',
            field=models.CharField(max_length=500, verbose_name='Слоган'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=150, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1895)], verbose_name='Год выхода'),
        ),
        migrations.AlterField(
            model_name='movietrailer',
            name='link',
            field=models.URLField(verbose_name='Ссылка на трейлер (youtube)'),
        ),
        migrations.AlterField(
            model_name='movietrailer',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trailers', to='movies.movie', verbose_name='Фильм'),
        ),
        migrations.AlterField(
            model_name='movietype',
            name='title',
            field=models.CharField(max_length=150, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='poster',
            name='format',
            field=models.CharField(choices=[('LARGE', 'Большой'), ('MEDIUM', 'Средний'), ('SMALL', 'Маленький')], max_length=10, verbose_name='Размер'),
        ),
        migrations.AlterField(
            model_name='poster',
            name='image',
            field=models.ImageField(storage=django_minio_backend.models.MinioBackend(bucket_name='images'), upload_to=django_minio_backend.models.iso_date_prefix, verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='poster',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posters', to='movies.movie', verbose_name='Фильм'),
        ),
        migrations.AlterField(
            model_name='poster',
            name='orientation',
            field=models.CharField(choices=[('VERTICAL', 'Вертикальный'), ('HORIZONTAL', 'Горизонтальный')], max_length=10, verbose_name='Ориентация'),
        ),
    ]
