# Generated by Django 3.2.19 on 2023-12-19 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lemmatized_text', '0020_lemmatizedtextbookmark_read_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='lemmatizedtextbookmark',
            name='started_read_at',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
    ]
