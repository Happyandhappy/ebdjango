# Generated by Django 2.1.1 on 2019-02-05 19:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20190204_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='daily_task_done_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 3, 20, 25, 23, 504006)),
        ),
    ]
