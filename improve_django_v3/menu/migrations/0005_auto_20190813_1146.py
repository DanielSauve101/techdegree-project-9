# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2019-08-13 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_auto_20190813_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='ingredients',
            field=models.ManyToManyField(related_name='ingredients', to='menu.Ingredient'),
        ),
    ]