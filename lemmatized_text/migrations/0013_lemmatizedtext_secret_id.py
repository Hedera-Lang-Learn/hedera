# Generated by Django 2.2.16 on 2020-10-12 23:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('lemmatized_text', '0012_auto_20200928_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='lemmatizedtext',
            name='secret_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
