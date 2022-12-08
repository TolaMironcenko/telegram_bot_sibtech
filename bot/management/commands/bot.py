from django.core.management.base import BaseCommand
from django.conf import settings
import telebot
from telebot import types
import time
from bot.models import Faq, ChatState, Mail
from pathlib import Path
import os


def set_state(user_id, status):
    ChatState.objects.update_or_create(chat_id=user_id, defaults={"state": status})


def get_state(user_id):
    state = ChatState.objects.get(chat_id=user_id)
    return state.state


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'error: {e}'
            print(error_message)
            raise e

    return inner


markup = types.ReplyKeyboardMarkup(row_width=2)
FAQbtn = types.KeyboardButton('FAQ')
mailing = types.KeyboardButton('Рассылки')
markup.row(FAQbtn, mailing)

NewMail = {"text": '', 'photo': '', 'auditory': ''}


class Command(BaseCommand):
    help = 'task1 bot'

    def handle(self, *args, **options):
        bot = telebot.TeleBot(settings.BOT_TOKEN)
        print(bot.get_me())

        @log_errors
        def main_bot(messages):
            for message in messages:
                if message.text is not None:
                    if message.text.split(' ')[0] == '/start':
                        print(message.chat.id)
                        set_state(message.chat.id, 0)
                        bot.send_message(message.chat.id, "Привет это чат поддержки", reply_markup=markup)

                    if message.text == 'FAQ':
                        faq_markup = types.InlineKeyboardMarkup()
                        allfaq = Faq.objects.filter(is_active=True)
                        for faqobj in allfaq:
                            faqbtn = types.InlineKeyboardButton(text=faqobj.question, callback_data=faqobj.question)
                            faq_markup.row(faqbtn)
                        bot.send_message(message.chat.id, "Какой у вас вопрос?", reply_markup=faq_markup)

                    if message.text == 'Рассылки':
                        set_state(message.chat.id, 1)
                        bot.send_message(message.chat.id, "Введите текст рассылки")

        @log_errors
        @bot.message_handler(func=lambda message: get_state(message.chat.id) == 1)
        def enter_text_to_send(message):
            print(message.text)
            NewMail['text'] = message.text
            set_state(message.chat.id, 2)
            bot.send_message(message.chat.id, "Прикрепите изображение")

        @log_errors
        @bot.message_handler(content_types=["photo"], func=lambda message: get_state(message.chat.id) == 2)
        def enter_photo(message):
            print(message.text)
            Path(os.path.join(settings.BASE_DIR, 'media') + f'/{message.chat.id}/').mkdir(parents=True, exist_ok=True)
            if message.content_type == 'photo':
                photo_id = message.photo[-1].file_id
                NewMail['photo'] = bot.get_file(photo_id).file_path
                downloaded_file = bot.download_file(bot.get_file(photo_id).file_path)
                # os.path.join(settings.BASE_DIR, 'media')
                src = f'media/{message.chat.id}/' + bot.get_file(
                    photo_id).file_path.replace('photos/', '')
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)
                NewMail['photo'] = f'{message.chat.id}/' + bot.get_file(
                    photo_id).file_path.replace('photos/', '')
                print(NewMail['photo'])
                all_ok_markup = types.InlineKeyboardMarkup()
                all_ok_markup.row(types.InlineKeyboardButton("Подтвердить", callback_data="yes_all_ok"))
                bot.send_photo(message.chat.id, downloaded_file, caption=NewMail['text'], reply_markup=all_ok_markup)
                # bot.send_message(message.chat.id, "Ваша заявка:\n", reply_markup=all_ok_markup)

        @log_errors
        @bot.message_handler(func=lambda message: get_state(message.chat.id) == 3)
        def enter_auditory(message):
            print(message.text)
            NewMail['auditory'] = message.text
            mail_to_db = Mail.objects.create(text=NewMail['text'], photo=NewMail['photo'], auditory=NewMail['auditory'])
            print(mail_to_db)
            mail_to_db.save()
            set_state(message.chat.id, 0)
            bot.send_message(message.chat.id, "Отлично. Ваша заявка принята")

        bot.set_update_listener(main_bot)

        @log_errors
        @bot.callback_query_handler(func=lambda call: True)
        def callback_answer(call):
            if call.data == "yes_all_ok":
                print(call.message.text)
                set_state(call.message.chat.id, 3)
                bot.send_message(call.message.chat.id, "Опишите целевую аудиторию для отправки email-рассылки")
            else:
                print(call.data)
                answer = Faq.objects.get(question=call.data)
                bot.send_message(call.message.chat.id, answer.answer)

        try:
            bot.polling(non_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)
            bot.polling(non_stop=True)
