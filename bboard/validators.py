from django.core.exceptions import ValidationError
def validate_positive_or_zero(value):
    if value < 0:
        raise ValidationError('Значение должно быть положительным или равно нулю')