# Generated by Django 2.2.13 on 2020-07-02 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_auto_20200603_1933'),
        ('lemmatized_text', '0009_lemmatizedtext_original_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='lemmatizedtext',
            name='cloned_for',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='groups.Group'),
        ),
    ]
