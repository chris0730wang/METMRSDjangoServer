# Generated by Django 3.1.1 on 2021-01-28 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20210128_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vocabularypreview',
            name='correctans',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='vocabularypreview',
            name='option4',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vocabularypreview',
            name='question',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='vocabularypreview',
            name='questionnum',
            field=models.CharField(max_length=100),
        ),
    ]
