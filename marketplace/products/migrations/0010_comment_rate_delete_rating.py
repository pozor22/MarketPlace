# Generated by Django 5.1.4 on 2025-01-29 21:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_comment_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='rate',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]
