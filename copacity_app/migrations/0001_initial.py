# Generated by Django 3.1.7 on 2021-03-27 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField(auto_now_add=True)),
                ('hardToday', models.CharField(max_length=200)),
                ('goodToday', models.CharField(max_length=200)),
                ('excitedToday', models.CharField(max_length=200)),
            ],
        ),
    ]
