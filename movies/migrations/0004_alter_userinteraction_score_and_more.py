# Generated by Django 4.2.4 on 2023-08-31 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_user_email_user_password_user_username_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinteraction',
            name='score',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userinteraction',
            name='visualization',
            field=models.BooleanField(default=False),
        ),
    ]
