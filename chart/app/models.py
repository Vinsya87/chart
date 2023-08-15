from django.db import models
from django.utils import timezone
from django.db.models import UniqueConstraint


class DataPoint(models.Model):
    date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания',
    )
    number = models.IntegerField(
        verbose_name='Значение',
    )

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d %H:%M:%S')} - {self.number}"

    class Meta:
        constraints = [
            UniqueConstraint(fields=['date'], name='unique_date_constraint')
        ]
