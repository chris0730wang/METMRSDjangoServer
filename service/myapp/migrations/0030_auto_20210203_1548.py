# Generated by Django 3.1.1 on 2021-02-03 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0029_auto_20210203_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='focusoncontent',
            name='option2',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='focusoncontent',
            name='option3',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='focusoncontent',
            name='option4',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='focusoncontent',
            name='option5',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
