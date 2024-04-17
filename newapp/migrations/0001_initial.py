# Generated by Django 4.2.6 on 2023-10-27 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('sex', models.CharField(max_length=15)),
                ('guest_count', models.IntegerField()),
                ('country', models.CharField(max_length=200)),
                ('comments', models.CharField(max_length=1000)),
                ('date', models.DateField(auto_now=True)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
