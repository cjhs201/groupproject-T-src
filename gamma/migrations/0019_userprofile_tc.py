# Generated by Django 3.1.7 on 2021-03-10 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamma', '0018_auto_20210310_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='tc',
            field=models.BooleanField(default=True),
        ),
    ]
