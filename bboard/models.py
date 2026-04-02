from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from .validators import validate_positive_or_zero


def validate_even(val):
    if val % 2 != 0:
        raise ValidationError('Число %(value)s нечётное', code='odd',
                              params={'value': val})

class MinMaxValueValidator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, val):
        if val < self.min_value or val > self.max_value:
            raise ValidationError('Введённое число должно'
                    'находиться в диапазоне от %(min)s до %(max)s',
                    code='out_of_range',
                    params={'min': self.min_value, 'max': self.max_value})

class Rubric(models.Model):
    name = models.CharField(
        unique=True,
        max_length=20,
        db_index=True,
        verbose_name='Название',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ['name']


class Bb(models.Model):
    # KINDS = (
    #     ('b', 'Куплю'),
    #     ('s', 'Продам'),
    #     ('c', 'Обменяю'),
    # )

    KINDS = (
        ('Купля-продажа', (
            ('b', 'Куплю'),
            ('s', 'Продам'),
        )),
        ('Обмен', (
            ('c', 'Обменяю'),
        ))
    )

    kind = models.CharField(
        max_length=1,
        choices=KINDS,
        default='s',
        verbose_name='Тип объявления',
    )

    title = models.CharField(
        max_length=50,
        verbose_name='Товар',
        validators=[
            validators.RegexValidator(regex='^.{4,}$'),
        ],
        error_messages={'invalid': 'Неправильное название товара'}
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
        max_digits=13,  # 12345678901,21
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
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика',
        # related_name='entries',
    )

    def title_and_price(self):
        if self.price:
            return f'{self.title} ({self.price:.2f})'

    title_and_price.short_description = 'Название и цена'

    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Укажите описание')

        if self.price and self.price < 0:
            errors['price'] = ValidationError(
                'Укажите неотрицательное значение цены')

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-published', 'title']
        # get_latest_by = ['edited', 'published']

    #dz
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#DZ 6 Models
# class Kiosk(models.Model):
#     name = models.CharField(max_length=100, verbose_name='Название киоска')
#     address = models.CharField(max_length=200, verbose_name='Адрес')
#
#     def __str__(self):
#         return self.name
#
#     def get_id_and_name(self):
#         return f'ID: {self.id}, Название: {self.name}'
#
#     def total_icecream_price(self):
#         return sum(ice_cream.price for ice_cream in self.ice_creams.all())
#
#
# class IceCream(models.Model):
#     kiosk = models.ForeignKey(
#         Kiosk,
#         on_delete=models.CASCADE,
#         related_name='ice_creams',
#         verbose_name='Киоск'
#     )
#     name = models.CharField(max_length=100, verbose_name='Название мороженого')
#     flavor = models.CharField(max_length=100, verbose_name='Вкус')
#     price = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         verbose_name='Цена',
#         validators=[validate_positive_or_zero]
#     )
#
#     def __str__(self):
#         return f'{self.name} - {self.flavor}'
#
#     def get_id_and_price(self):
#         return f'ID: {self.id}, Цена: {self.price}'
#
#
# class Parent(models.Model):
#     first_name = models.CharField(max_length=100, verbose_name='Имя')
#     last_name = models.CharField(max_length=100, verbose_name='Фамилия')
#     age = models.PositiveIntegerField(
#         verbose_name='Возраст',
#         validators=[validate_positive_or_zero]
#     )
#
#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'
#
#     def get_id_and_age(self):
#         return f'ID: {self.id}, Возраст: {self.age}'
#
#     def total_children_age(self):
#         return sum(child.age for child in self.children.all())
#
#
# class Child(models.Model):
#     parent = models.ForeignKey(
#         Parent,
#         on_delete=models.CASCADE,
#         related_name='children',
#         verbose_name='Родитель'
#     )
#     first_name = models.CharField(max_length=100, verbose_name='Имя')
#     age = models.PositiveIntegerField(
#         verbose_name='Возраст',
#         validators=[validate_positive_or_zero]
#     )
#
#     def __str__(self):
#         return self.first_name
#
#     def get_id_and_age(self):
#         return f'ID: {self.id}, Возраст: {self.age}'

# DZ LIST ZADACH
# class Task(models.Model):
#     title = models.CharField('Название', max_length=200)
#     description = models.TextField('Описание', blank=True)
#     is_done = models.BooleanField('Выполнено', default=False)
#     priority = models.IntegerField('Приоритет', default=1)
#     created_at = models.DateTimeField('Создано', auto_now_add=True)
#
#     class Meta:
#         ordering = ['is_done', '-priority', '-created_at']
#         verbose_name = 'Задача'
#         verbose_name_plural = 'Задачи'
#
#     def __str__(self):
#         return self.title
#
#     def get_absolute_url(self):
#         return reverse('tasks:task_detail', kwargs={'pk':self.pk})