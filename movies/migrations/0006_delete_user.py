# Generated by Django 4.2.4 on 2023-08-31 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_alter_userinteraction_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
