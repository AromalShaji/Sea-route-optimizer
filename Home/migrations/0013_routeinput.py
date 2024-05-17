# Generated by Django 5.0.3 on 2024-04-20 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0012_alter_crew_ship'),
    ]

    operations = [
        migrations.CreateModel(
            name='RouteInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lon_st', models.FloatField()),
                ('lat_st', models.FloatField()),
                ('lon_de', models.FloatField()),
                ('lat_de', models.FloatField()),
                ('stTime', models.CharField(max_length=100)),
                ('eTime', models.CharField(max_length=100)),
                ('generation_count', models.IntegerField()),
                ('pop_size', models.IntegerField()),
                ('offspring', models.IntegerField()),
                ('lon_min', models.IntegerField()),
                ('lon_max', models.IntegerField()),
                ('lat_min', models.IntegerField()),
                ('lat_max', models.IntegerField()),
                ('draft', models.FloatField()),
            ],
        ),
    ]
