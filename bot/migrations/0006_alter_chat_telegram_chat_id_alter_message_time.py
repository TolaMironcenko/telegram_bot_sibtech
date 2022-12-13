# Generated by Django 4.1.4 on 2022-12-13 03:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_alter_chat_username_alter_message_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='telegram_chat_id',
            field=models.TextField(verbose_name='Чат id пользователя'),
        ),
        migrations.AlterField(
            model_name='message',
            name='time',
            field=models.TimeField(default=datetime.datetime(2022, 12, 13, 10, 30, 31, 678238), verbose_name='Время отправки'),
        ),
    ]
