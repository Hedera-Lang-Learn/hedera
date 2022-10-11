# Generated by Django 3.2.15 on 2022-09-30 19:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocab_list', '0013_auto_20220914_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalvocabularylistentry',
            name='familiarity',
            field=models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)]),
        ),
    ]