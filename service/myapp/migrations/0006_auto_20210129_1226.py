# Generated by Django 3.1.1 on 2021-01-29 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20210128_1758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vocabularypreview',
            old_name='lesson',
            new_name='reading',
        ),
        migrations.RenameField(
            model_name='vocabularypreviewans',
            old_name='lesson',
            new_name='reading',
        ),
    ]
