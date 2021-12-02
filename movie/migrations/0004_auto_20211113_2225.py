# Generated by Django 3.2.9 on 2021-11-13 20:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_auto_20211111_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='moviePlatform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stream', to='movie.streamplatform'),
        ),
        migrations.CreateModel(
            name='review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('review_movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='movie.movie')),
            ],
        ),
    ]