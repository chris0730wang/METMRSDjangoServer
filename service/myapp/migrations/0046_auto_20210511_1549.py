# Generated by Django 3.1.1 on 2021-05-11 15:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0045_auto_20210511_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='u10r1focusoncontentans',
            name='q8answer',
            field=models.CharField(default='no', max_length=255),
        ),
        migrations.AlterField(
            model_name='setnaoip',
            name='timezone',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 11, 15, 49, 2, 123533)),
        ),
    ]