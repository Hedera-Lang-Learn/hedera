# Generated by Django 2.1.7 on 2019-02-28 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lemmatized_text', '0002_lemmatizedtext_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='lemmatizedtext',
            name='lang',
            field=models.CharField(default='grc', max_length=3),
            preserve_default=False,
        ),
    ]
