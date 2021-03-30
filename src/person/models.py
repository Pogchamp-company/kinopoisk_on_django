from itertools import starmap
from typing import TYPE_CHECKING

from django.db import models
from django.utils.functional import cached_property
from utils.enums import ChoiceEnum
from utils.mixins import Image, ImageProperties
from datetime import date, datetime
import bisect

if TYPE_CHECKING:
    from movies.models import Movie


class Photo(Image):
    person = models.ForeignKey('Person', related_name='photos', on_delete=models.CASCADE)


class PersonRole(models.Model):
    class RoleType(ChoiceEnum):
        DIRECTOR = 'Режиссер'
        WRITER = 'Сценарист'
        PRODUCER = 'Продюсер'
        OPERATOR = 'Оператор'
        COMPOSER = 'Композитор'
        EDITOR = 'Монтажер'
        ACTOR = 'Актер'
        DESIGN = 'Постановщик'
        VOICE_DIRECTOR = 'Звукорежиссер'
        TRANSLATOR = 'Переводчик'

    role_name = models.CharField(max_length=1000, null=True)
    role_type = models.CharField(max_length=20, choices=RoleType.choices())

    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='roles')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='roles')

    def __str__(self):
        f_role_name = f' ({self.role_name})' if self.role_name else ''
        return f'<{self.__class__.__name__} ({self.person}, ' \
               f'{getattr(self.RoleType, self.role_type).value}{f_role_name}, {self.movie})>'


class Person(models.Model, ImageProperties):
    fullname = models.CharField(max_length=150)
    ru_fullname = models.CharField(max_length=150, null=True)

    birth_date = models.DateField(null=True)
    death = models.DateField(null=True)

    # САНТИМЕТРы)))))
    height = models.PositiveIntegerField(null=True)

    class SexEnum(ChoiceEnum):
        MALE = 'Мужчина'
        FEMALE = 'Женщина'

    sex = models.CharField(max_length=6, choices=SexEnum.choices())

    movies = models.ManyToManyField('movies.Movie', through='PersonRole', related_name='persons')

    @property
    def movies_genres(self) -> set['Movie']:
        genres = set()
        for movie in self.movies.all():
            genres = genres.union(movie.genres.all())
        return genres

    @property
    def movies_info(self) -> str:
        query = self.movies.order_by('year')
        return f'{len(set(self.movies.all()))}, {query.first().year} - {query.last().year}'

    @cached_property
    def existing_roles(self) -> list[PersonRole.RoleType]:
        return list(filter(lambda rel_name: self.roles.filter(role_type=rel_name.name).exists(),
                           PersonRole.RoleType))

    @cached_property
    def roles_with_movies(self) -> list[tuple[PersonRole.RoleType, list['Movie']]]:
        return [(role, list(map(lambda role: role.movie, roles))) for role in PersonRole.RoleType if
                (roles := self.roles.filter(role_type=role.name).all())]

    @property
    def formatted_roles(self) -> list[str]:
        return list(starmap(lambda role_type, _: role_type.value, self.roles_with_movies))

    @property
    def age_word(self) -> str:
        last_digit_of_age = self.age % 10
        if last_digit_of_age == 1:
            return 'год'
        if 2 <= last_digit_of_age <= 4:
            return 'года'
        return 'лет'

    @cached_property
    def age(self) -> int:
        today = date.today()
        try:
            birthday = self.birth_date.replace(year=today.year)
        except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = self.birth_date.replace(year=today.year, month=self.birth_date.month + 1, day=1)
        return today.year - self.birth_date.year - 1 if birthday > today else today.year - self.birth_date.year

    @property
    def zodiac_sign(self) -> str:
        tdays = [19, 49, 80, 110, 141, 173, 204,
                 235, 256, 296, 327, 356, 366]
        zod = ["Козерог", "Водолей", "Рыбы", "Овен",
               "Телец", "Близнецы", "Рак", "Лев",
               "Дева", "Весы", "Скорпион",
               "Стрелец", "Козерог"]
        d, m = self.birth_date.day, self.birth_date.month
        return zod[bisect.bisect_left(tdays, (datetime(2021, m, d) - datetime(2020, 12, 31)).days)]

    @property
    def formatted_birth_date(self) -> str:
        if not self.birth_date:
            return '-'
        months = ('января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                  'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря')

        return f'{self.birth_date.day} {months[self.birth_date.month - 1]}, ' \
               f'{self.birth_date.year} • {self.zodiac_sign} • {self.age} {self.age_word}'

    def __str__(self):
        return self.ru_fullname or self.fullname

    @property
    def images(self):
        return self.photos

    @property
    def default_images_folder(self) -> str:
        return 'icon/default_photos'
