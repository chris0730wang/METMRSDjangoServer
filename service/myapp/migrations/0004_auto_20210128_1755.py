# Generated by Django 3.1.1 on 2021-01-28 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20210128_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vocabularypreview',
            name='correctans',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vocabularypreview',
            name='question',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vocabularypreview',
            name='questionnum',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
