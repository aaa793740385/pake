# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-22 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0004_userinformation_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='content',
            field=models.TextField(default='image/girl.jpg', max_length=100),
        ),
    ]