# Generated by Django 3.1.7 on 2021-03-09 22:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamma', '0013_auto_20210309_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]