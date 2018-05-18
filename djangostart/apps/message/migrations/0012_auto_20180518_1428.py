# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-18 06:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0011_userinformation_crawl_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='CloudMusicInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('star_id', models.IntegerField()),
                ('star_name', models.CharField(max_length=32)),
            ],
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='crawl_time',
            field=models.CharField(default='0', max_length=100),
        ),
    ]
