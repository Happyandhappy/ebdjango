# Generated by Django 2.1.7 on 2019-03-27 15:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20190327_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='completed_at',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='daily_task_done_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 25, 16, 23, 30, 255853)),
        ),
    ]
