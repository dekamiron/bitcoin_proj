# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-13 13:06
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hash', '0003_auto_20180513_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hash',
            name='value',
            field=models.CharField(max_length=64, validators=[django.core.validators.MinLengthValidator(64)]),
        ),
    ]