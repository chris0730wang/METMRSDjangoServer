# Generated by Django 3.1.1 on 2021-05-26 13:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0059_auto_20210526_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setnaoip',
            name='timezone',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 26, 13, 30, 8, 956523)),
        ),
        migrations.AlterField(
            model_name='setstarttime',
            name='timezone',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 26, 13, 30, 8, 957520)),
        ),
    ]