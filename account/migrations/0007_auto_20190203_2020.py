# Generated by Django 2.1.1 on 2019-02-03 19:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20190203_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='daily_task_done_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 1, 20, 20, 23, 629801)),
        ),
    ]
