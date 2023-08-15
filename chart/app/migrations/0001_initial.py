# Generated by Django 4.1 on 2023-08-15 03:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('number', models.IntegerField(verbose_name='Значение')),
            ],
        ),
        migrations.AddConstraint(
            model_name='datapoint',
            constraint=models.UniqueConstraint(fields=('date',), name='unique_date_constraint'),
        ),
    ]
