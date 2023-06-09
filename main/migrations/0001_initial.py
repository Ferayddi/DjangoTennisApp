# Generated by Django 4.1.5 on 2023-02-01 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='priority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_email', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='sessions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=250)),
                ('member_email', models.CharField(max_length=250)),
                ('session_choice', models.IntegerField()),
                ('session_flexible', models.BooleanField(default=0)),
                ('session_assigned', models.IntegerField(default=0)),
                ('attended', models.BooleanField(default=0)),
            ],
        ),
    ]
