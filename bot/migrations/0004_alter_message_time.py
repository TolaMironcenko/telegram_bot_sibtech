# Generated by Django 4.1.4 on 2022-12-10 17:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_alter_message_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='time',
            field=models.TimeField(default=datetime.datetime(2022, 12, 11, 0, 58, 0, 660785), verbose_name='Время отправки'),
        ),
    ]
