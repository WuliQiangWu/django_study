# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-12 17:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='image',
            field=models.ImageField(max_length=200, upload_to='org/%Y/%m', verbose_name='\u5c01\u9762'),
        ),
    ]
