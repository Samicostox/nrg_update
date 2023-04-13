# Generated by Django 4.0.2 on 2022-11-30 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_userproduction_windturbine_userconsumption_tv_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='solarpanel',
            name='is_on',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tv',
            name='is_on',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='windturbine',
            name='is_on',
            field=models.BooleanField(default=False),
        ),
    ]
