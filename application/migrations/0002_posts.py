# Generated by Django 4.0.5 on 2022-06-22 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('userID', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('body', models.CharField(max_length=1000)),
            ],
        ),
    ]
