# Generated by Django 3.2.19 on 2024-02-16 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lemmatization', '0005_delete_latinlexicon'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='formtolemma',
            options={'verbose_name': 'Form to Lemma', 'verbose_name_plural': 'Form to Lemmas'},
        ),
        migrations.AlterModelOptions(
            name='gloss',
            options={'ordering': ['lemma', 'gloss'], 'verbose_name': 'Gloss', 'verbose_name_plural': 'Glosses'},
        ),
        migrations.AlterModelOptions(
            name='lemma',
            options={'verbose_name': 'Lemma', 'verbose_name_plural': 'Lemmas'},
        ),
    ]
