# Generated by Django 2.2.3 on 2019-08-27 15:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lemmatized_text', '0006_lemmatizedtext_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='lemmatizedtext',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='lemmatizedtext',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lemmatizedtext',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
