# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-14 18:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_id', models.CharField(max_length=500, unique=True)),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('detail_info', models.TextField()),
                ('price', models.DecimalField(decimal_places=4, max_digits=10)),
                ('rating', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cover_large', models.ImageField(upload_to='')),
                ('cover_small', models.ImageField(upload_to='')),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=500)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screenshots', to='core.App')),
            ],
        ),
        migrations.AddField(
            model_name='app',
            name='developer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apps', to='core.Developer'),
        ),
        migrations.AddField(
            model_name='app',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
