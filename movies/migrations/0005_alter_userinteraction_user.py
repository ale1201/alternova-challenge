# Generated by Django 4.2.4 on 2023-08-31 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_alter_userinteraction_score_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinteraction',
            name='user',
            field=models.CharField(max_length=200),
        ),
    ]
