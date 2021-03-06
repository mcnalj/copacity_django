# Generated by Django 3.1.7 on 2021-04-19 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copacity_app', '0004_auto_20210419_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='actions',
            field=models.IntegerField(choices=[(1, 'Yes'), (2, 'No'), (3, 'Maybe')], default=0),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='thoughts',
            field=models.IntegerField(choices=[(1, 'Yes'), (2, 'No'), (3, 'Maybe')], default=0),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='urgency',
            field=models.IntegerField(choices=[(1, 'Call now'), (2, 'Text now'), (3, 'Talk later'), (4, 'Not necessary to talk about it'), (5, 'I Prefer not to talk about it')], default=4),
        ),
    ]
