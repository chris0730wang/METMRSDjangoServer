# Generated by Django 3.1.1 on 2021-01-29 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20210129_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vocabularypreview',
            name='falsepercent',
            field=models.IntegerField(null=True),
        ),
    ]
