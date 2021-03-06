# Generated by Django 4.0 on 2021-12-11 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_code', models.CharField(max_length=4)),
                ('flight_location', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=50)),
                ('departuredate', models.CharField(max_length=10)),
                ('returndate', models.CharField(max_length=10)),
                ('flightfrom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='flight_register.flight')),
                ('flightto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='flight_register.flight')),
            ],
        ),
    ]
