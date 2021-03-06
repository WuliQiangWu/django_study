# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-20 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20171212_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='category',
            field=models.CharField(choices=[('pxjg', '\u57f9\u8bad\u673a\u6784'), ('gr', '\u4e2a\u4eba'), ('gx', '\u9ad8\u6821')], default='pxjjg', max_length=20, verbose_name='\u673a\u6784\u7c7b\u522b'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='image',
            field=models.ImageField(max_length=200, upload_to='org/%Y/%m', verbose_name='logo'),
        ),
    ]
