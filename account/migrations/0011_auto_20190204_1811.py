# Generated by Django 2.1.1 on 2019-02-04 17:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20190203_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='daily_task_done_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 2, 18, 11, 34, 836392)),
        ),
    ]
