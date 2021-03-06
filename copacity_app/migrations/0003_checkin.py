# Generated by Django 3.1.7 on 2021-04-19 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copacity_app', '0002_auto_20210416_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField(auto_now_add=True)),
                ('yourName', models.IntegerField(default=0)),
                ('hardToday', models.CharField(max_length=200)),
                ('goodToday', models.CharField(max_length=200)),
                ('excitedToday', models.CharField(max_length=200)),
                ('thoughts', models.IntegerField(default=0)),
                ('thoughtsExplained', models.CharField(max_length=400)),
                ('actions', models.IntegerField(default=0)),
                ('actionsExplained', models.CharField(max_length=400)),
                ('moodRange', models.IntegerField(default=5)),
                ('pintaRange', models.IntegerField(default=5)),
                ('urgency', models.IntegerField(default=4)),
            ],
        ),
    ]
