# Generated by Django 3.2.7 on 2021-09-08 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lemmatized_text', '0016_merge_20210812_2010'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lemmatizedtextbookmark',
            options={'ordering': ['-created_at'], 'verbose_name': 'lemmatized text bookmark', 'verbose_name_plural': 'lemmatized text bookmarks'},
        ),
        migrations.AlterField(
            model_name='lemmatizedtext',
            name='data',
            field=models.JSONField(),
        ),
    ]
