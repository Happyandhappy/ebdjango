# Generated by Django 2.1.1 on 2019-02-03 20:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20190203_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='daily_task_done_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 1, 21, 48, 9, 289663)),
        ),
    ]