# Generated by Django 4.1.4 on 2022-12-12 10:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_alter_message_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='username',
            field=models.TextField(verbose_name='Username telegram'),
        ),
        migrations.AlterField(
            model_name='message',
            name='time',
            field=models.TimeField(default=datetime.datetime(2022, 12, 12, 17, 46, 44, 357798), verbose_name='Время отправки'),
        ),
    ]