# Generated by Django 4.0.2 on 2023-02-13 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_rename_is_consuming_object_is_consuming_object'),
    ]

    operations = [
        migrations.RenameField(
            model_name='object',
            old_name='account',
            new_name='owner',
        ),
    ]