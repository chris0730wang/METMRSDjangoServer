# Generated by Django 3.1.1 on 2021-05-11 20:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0048_auto_20210511_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setnaoip',
            name='timezone',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 11, 20, 27, 33, 656147)),
        ),
    ]
