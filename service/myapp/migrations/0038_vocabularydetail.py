# Generated by Django 3.1.1 on 2021-03-08 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0037_auto_20210226_1310'),
    ]

    operations = [
        migrations.CreateModel(
            name='VocabularyDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('unit', models.IntegerField()),
                ('reading', models.IntegerField()),
                ('num', models.IntegerField()),
                ('vocabulary', models.CharField(max_length=100)),
                ('partsofspeech', models.CharField(max_length=100)),
                ('explain', models.CharField(max_length=100)),
            ],
        ),
    ]
