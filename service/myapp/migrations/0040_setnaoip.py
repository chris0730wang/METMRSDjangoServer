# Generated by Django 3.1.1 on 2021-05-02 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0039_auto_20210408_1812'),
    ]

    operations = [
        migrations.CreateModel(
            name='SetNaoIP',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('IPAddress', models.CharField(max_length=100)),
                ('timezone', models.DateTimeField()),
            ],
        ),
    ]