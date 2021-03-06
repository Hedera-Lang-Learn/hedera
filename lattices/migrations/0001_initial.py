# Generated by Django 2.1.5 on 2019-02-01 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.CharField(blank=True, max_length=255)),
                ('form', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='LatticeNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.TextField()),
                ('children', models.ManyToManyField(to='lattices.LatticeNode')),
            ],
        ),
        migrations.CreateModel(
            name='LemmaNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.CharField(blank=True, max_length=255)),
                ('lemma', models.CharField(max_length=255)),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lemma_strings', to='lattices.LatticeNode')),
            ],
        ),
        migrations.AddField(
            model_name='formnode',
            name='node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_strings', to='lattices.LatticeNode'),
        ),
    ]
