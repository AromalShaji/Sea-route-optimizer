# Generated by Django 3.2.12 on 2024-03-07 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0010_ship_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crew',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crew',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
