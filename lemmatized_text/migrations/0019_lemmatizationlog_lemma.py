# Generated by Django 3.2.15 on 2022-09-27 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lemmatization', '0005_delete_latinlexicon'),
        ('lemmatized_text', '0018_remove_lemmatizationlog_node'),
    ]

    operations = [
        migrations.AddField(
            model_name='lemmatizationlog',
            name='lemma',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lemmatization.lemma'),
        ),
    ]
