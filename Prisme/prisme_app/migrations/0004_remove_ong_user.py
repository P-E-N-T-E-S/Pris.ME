# Generated by Django 4.2.5 on 2023-10-14 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prisme_app', '0003_ong_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ong',
            name='user',
        ),
    ]
