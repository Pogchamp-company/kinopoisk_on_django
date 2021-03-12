from django.db import models
from django.utils.functional import cached_property

from utils.mixins import Image
from datetime import date, datetime
import bisect


class Photo(Image):
    person = models.ForeignKey('Person', related_name='photos', on_delete=models.CASCADE)


class Person(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=100)

    birth_date = models.DateField()

    # САНТИМЕТРы)))))
    height = models.PositiveIntegerField()

    @property
    def age_word(self):
        last_digit_of_age = self.age % 10
        if last_digit_of_age == 1:
            return 'год'
        if 2 <= last_digit_of_age <= 4:
            return 'года'
        return 'лет'

    @cached_property
    def age(self):
        today = date.today()
        try:
            birthday = self.birth_date.replace(year=today.year)
        except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = self.birth_date.replace(year=today.year, month=self.birth_date.month + 1, day=1)
        return today.year - self.birth_date.year - 1 if birthday > today else today.year - self.birth_date.year

    @property
    def zodiac_sign(self):
        tdays = [19, 49, 80, 110, 141, 173, 204,
                 235, 256, 296, 327, 356, 366]
        zod = ["Козерог", "Водолей", "Рыбы", "Овен",
               "Телец", "Близнецы", "Рак", "Лев",
               "Дева", "Весы", "Скорпион",
               "Стрелец", "Козерог"]
        d, m = self.birth_date.day, self.birth_date.month
        return zod[bisect.bisect_left(tdays, (datetime(2021, m, d) - datetime(2020, 12, 31)).days)]

    @property
    def formatted_birth_date(self):
        months = ('января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                  'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря')

        return f'{self.birth_date.day} {months[self.birth_date.month - 1]}, {self.birth_date.year} • {self.zodiac_sign} • {self.age} {self.age_word}'

    @property
    def fullname(self):
        return f'{self.name} {self.surname}'

    def __str__(self):
        return self.fullname