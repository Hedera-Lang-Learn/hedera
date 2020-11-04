# Generated by Django 2.2.16 on 2020-10-22 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocab_list', '0008_auto_20191115_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalvocabularylistentry',
            name='link_job_ended',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='personalvocabularylistentry',
            name='link_job_id',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='personalvocabularylistentry',
            name='link_job_started',
            field=models.DateTimeField(null=True),
        ),
    ]
