# Generated by Django 3.1.1 on 2021-05-26 18:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0061_auto_20210526_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setnaoip',
            name='timezone',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 26, 18, 4, 34, 923137)),
        ),
        migrations.AlterField(
            model_name='setstarttime',
            name='timezone',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 26, 18, 4, 34, 923137)),
        ),
    ]
