# Generated by Django 3.1.7 on 2021-06-22 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copacity_app', '0011_auto_20210621_1824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkin',
            name='visibility',
        ),
        migrations.AddField(
            model_name='checkin',
            name='visibility',
            field=models.ManyToManyField(blank=True, null=True, related_name='visibility', to='copacity_app.Circle'),
        ),
    ]
