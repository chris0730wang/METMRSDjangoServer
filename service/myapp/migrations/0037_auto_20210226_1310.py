# Generated by Django 3.1.1 on 2021-02-26 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0036_auto_20210225_1111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentcheck',
            old_name='focpoint',
            new_name='foc1point',
        ),
        migrations.RenameField(
            model_name='studentcheck',
            old_name='vppoint',
            new_name='foc2point',
        ),
        migrations.RenameField(
            model_name='studentcheck',
            old_name='vrpoint',
            new_name='vp1point',
        ),
        migrations.AddField(
            model_name='studentcheck',
            name='vp2point',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='studentcheck',
            name='vr1point',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='studentcheck',
            name='vr2point',
            field=models.IntegerField(null=True),
        ),
    ]