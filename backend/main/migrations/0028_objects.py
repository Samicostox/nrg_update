# Generated by Django 4.0.2 on 2023-02-13 19:47

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_consumingobject_expense_per_day_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Objects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_consuming', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('SOLAR_PANEL', 'solar_panel'), ('WIND_TURBINE', 'wind_turbine'), ('HEATING', 'heating'), ('COOLING', 'cooling'), ('TV', 'tv'), ('LIGHTING', 'lighting'), ('WASHER', 'washer'), ('DRYER', 'dryer'), ('REFREGIRATOR', 'refregirator')], default='HEATING', max_length=20)),
                ('energy_per_minute', models.IntegerField(default=10)),
                ('is_on', models.BooleanField(default=False)),
                ('overall_energy', models.IntegerField(default=0)),
                ('overall_expense', models.IntegerField(default=0)),
                ('number', models.IntegerField(default=0)),
                ('room', models.CharField(default='', max_length=50)),
                ('model_reference', models.CharField(default='', max_length=50)),
                ('name', models.CharField(default='', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('energy_per_day', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None)),
                ('todays_energy', models.IntegerField(default=0)),
                ('expense_per_day', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None)),
                ('todays_expense', models.IntegerField(default=0)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='object', to='main.account')),
            ],
        ),
    ]