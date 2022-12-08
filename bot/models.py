from django.db import models


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
        verbose_name='Текст рассылки'
    )
    photo = models.FileField(
        verbose_name='Изображение',
        upload_to='media/',
    )
    auditory = models.TextField(
        verbose_name='Целевая аудитория'
    )

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f'{self.text}'
