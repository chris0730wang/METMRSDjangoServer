# Generated by Django 3.1.1 on 2021-01-31 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_auto_20210131_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='u5beforeyoureadans',
            name='cId',
            field=models.CharField(default='NULL', max_length=10),
        ),
        migrations.AddField(
            model_name='u7beforeyoureadans',
            name='cId',
            field=models.CharField(default='NULL', max_length=10),
        ),
    ]