# Generated by Django 4.2.4 on 2023-08-30 23:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(default='example@example.com', max_length=200),
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='123', max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='test', max_length=50),
        ),
        migrations.AlterField(
            model_name='movie',
            name='score',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(5.0, message='El valor debe ser menor o igual a 5.'), django.core.validators.MinValueValidator(0.0, message='El valor debe ser mayor o igual a 1.')]),
        ),
        migrations.CreateModel(
            name='UserInteraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visualization', models.BooleanField()),
                ('score', models.BooleanField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.user')),
            ],
        ),
    ]
