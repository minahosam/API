# Generated by Django 3.2.9 on 2021-11-17 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0005_auto_20211115_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='avg_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='people_rating',
            field=models.IntegerField(default=0),
        ),
    ]
