from django.db import models

class Bb(models.Model):
    title = models.CharField(
        max_length=50,
    )
    content = models.TextField(
        null=True,
        blank=True,
    )

    price = models.DecimalField(
        null=True,
        blank=True,
        max_digits=13,
        decimal_places=2,
    )

    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )