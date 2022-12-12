from django.db import models
import datetime


class Faq(models.Model):
    question = models.TextField(
        verbose_name='Вопрос',
        null=False,
        primary_key=True,
        unique=True
    )
    answer = models.TextField(
        verbose_name='Ответ',
        null=False,
    )
    is_active = models.BooleanField(
        verbose_name='Доступно?',
        default=False
    )

    class Meta:
        verbose_name = 'Вопрос, ответ'
        verbose_name_plural = 'Вопроросы, ответы'

    def __str__(self):
        return f'{self.question} {self.answer}'


class ChatState(models.Model):
    chat_id = models.TextField(
        verbose_name='Имя пользователя в телеграм',
        primary_key=True,
        unique=True
    )
    state = models.IntegerField(
        verbose_name='Состояние',
        primary_key=False,
        unique=False,
        null=False
    )

    class Meta:
        verbose_name = 'Состояние для бота',
        verbose_name_plural = 'Состояния для бота'

    def __str__(self):
        return f'{self.chat_id, self.state}'


class Mail(models.Model):
    text = models.TextField(
        verbose_name='Текст заявки'
    )
    photo = models.FileField(
        verbose_name='Изображение',
        upload_to='media/',
    )
    auditory = models.TextField(
        verbose_name='Целевая аудитория'
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'{self.text}'


class Message(models.Model):
    text = models.TextField(
        verbose_name='Текст сообщения',
        null=False
    )
    time = models.TimeField(
        verbose_name='Время отправки',
        default=datetime.datetime.now()
    )
    from_user = models.TextField(
        verbose_name='От кого',
        default='telegram'
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.text}'


class Chat(models.Model):
    telegram_chat_id = models.TextField(
        verbose_name='Чат id пользователя',
        unique=True
    )
    username = models.TextField(
        verbose_name='Username telegram',
    )
    name = models.TextField(
        verbose_name='Имя пользователя telegram'
    )
    avatar = models.FileField(
        verbose_name='Аватар пользователя в телеграм',
        upload_to='media/',
        default='usericon.png'
    )
    messages = models.ManyToManyField(
        Message,
        verbose_name='Сообщения',
        blank=True
    )

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    def __str__(self):
        return f'{self.telegram_chat_id} {self.username} {self.name}'

