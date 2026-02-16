from email.policy import default
from random import choices
from wsgiref.validate import validator

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models

def validate_even(val):
    if val % 2 != 0:
        raise ValidationError('Число %(value)s нечетное', code='odd', params={'value': val})

class MinMaxValueValidator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, val):
        if val < self.min_value or val > self.max_value:
            raise ValidationError('Введенное число должно'
                                  'находиться в диапозоне от %(min)s до %(max)s',
                                  code='out_of_range',
                                  params={'min': self.min_value, 'max': self.max_value})

class Rubric(models.Model):
    name = models.CharField(
        unique=True,
        max_length=20,
        db_index=True,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Рубрика',
        verbose_name_plural = 'Рубрики',
        ordering = ['name']

class Bb(models.Model):
    KINDS  = (
        ('Купля-продажа', (
            ('b', 'Куплю'),
            ('s', 'Продам'),
        )),
        ('Обмен', (
            ('c', 'Обменяю'),
        )),
    )

    kind = models.CharField(
        max_length=1,
        choices=KINDS,
        default='s',
    )

    title = models.CharField(
        primary_key=True,
        max_length=50,
        verbose_name='Товар',
        validators=[
            validators.RegexValidator(regex='^.{4,}$'),
        ],
        error_messages={'invalid': 'Неправильно название товара'}
    )

    content = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )

    price = models.DecimalField(
        default=0,
        null=True,
        blank=True,
        max_digits=13,
        decimal_places=2,
        verbose_name='Цена',
        validators=[validate_even],
    )

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Опубликовано',
    )

    rubric = models.ForeignKey(
        'Rubric',
        null = True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика',
    )

    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Укажите описание')

        if self.price and self.price < 0:
            errors['price'] = ValidationError('Укажите неотрицательное значение цены')

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-published', 'title']
