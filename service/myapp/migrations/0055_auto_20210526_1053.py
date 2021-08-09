# Generated by Django 3.1.1 on 2021-05-26 10:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0054_auto_20210525_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schoolClass', models.CharField(max_length=20)),
                ('className', models.CharField(max_length=20)),
                ('schoolClassChinese', models.CharField(max_length=20)),
                ('seatNumber', models.CharField(max_length=20)),
                ('studentID', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=30)),
                ('identityCard', models.CharField(max_length=30)),
                ('sex', models.CharField(max_length=2)),
                ('birth_date', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='setnaoip',
            name='timezone',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 26, 10, 52, 58, 771102)),
        ),
        migrations.AlterField(
            model_name='setstarttime',
            name='timezone',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 26, 10, 52, 58, 771102)),
        ),
    ]