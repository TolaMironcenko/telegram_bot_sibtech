from django.core.management.base import BaseCommand
from django.conf import settings
import telebot
from telebot import types
import time
from bot.models import Faq, ChatState, Mail, Message, Chat
from pathlib import Path
import os
import datetime
from bitrix24 import *


def set_state(user_id, status):
    ChatState.objects.update_or_create(chat_id=user_id, defaults={"state": status})


def get_state(user_id):
    try:
        state = ChatState.objects.get(chat_id=user_id)
        return state.state
    except Exception as e:
        print(str(e))
        return 0


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
appeal = types.KeyboardButton('Создать обращение')
openline = types.InlineKeyboardButton(text='Открытая линия', url='https://t.me/bitrix24_test_tolamiron_bot')
markup.row(FAQbtn, mailing)
markup.row(appeal, openline)

NewMail = {"text": '', 'photo': '', 'auditory': ''}
bot = telebot.TeleBot(settings.BOT_TOKEN)


class Command(BaseCommand):
    help = 'task1 bot'

    def handle(self, *args, **options):

        @log_errors
        def main_bot(messages):
            for message in messages:
                # print(message)
                if message.content_type != 'text' and get_state(message.chat.id) == 1:
                    bot.send_message(message.chat.id, "Необходимо ввести текст рассылки")
                elif message.content_type != 'photo' and get_state(message.chat.id) == 2:
                    bot.send_message(message.chat.id, "Необходимо прикрепить изображение")
                elif message.content_type != 'text' and get_state(message.chat.id) == 3:
                    bot.send_message(message.chat.id,
                                     "Необходимо описать текстом целевую аудиторию для отправки email-рассылки")
                elif message.content_type != 'text' and get_state(message.chat.id) == 4:
                    bot.send_message(message.chat.id, "Необходимо ввести текст обращения")
                elif message.content_type != 'text' and get_state(message.chat.id) == 5:
                    bot.send_message(message.chat.id, 'Необходимо ввести именно текст сообщения для оператора поддержки')
                if message.text is not None:
                    if message.text.split(' ')[0] == '/start':
                        # print(message.chat.id)
                        set_state(message.chat.id, 0)
                        bot.send_message(message.chat.id, "Привет это чат поддержки", reply_markup=markup)

                    if message.text == 'FAQ':
                        set_state(message.chat.id, 0)
                        faq_markup = types.InlineKeyboardMarkup()
                        allfaq = Faq.objects.filter(is_active=True)
                        for faqobj in allfaq:
                            faqbtn = types.InlineKeyboardButton(text=faqobj.question, callback_data=faqobj.question)
                            faq_markup.row(faqbtn)
                        bot.send_message(message.chat.id, "Какой у вас вопрос?", reply_markup=faq_markup)

                    if message.text == 'Рассылки':
                        set_state(message.chat.id, 1)
                        bot.send_message(message.chat.id, "Введите текст рассылки")

                    if message.text == 'Создать обращение':
                        set_state(message.chat.id, 4)
                        bot.send_message(message.chat.id, 'Введите текст обращения')

                    if message.text == 'Открытая линия':
                        set_state(message.chat.id, 5)
                        bot.send_message(message.chat.id, 'Переходите в чат открытой линии', reply_markup=types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(text='Открытая линия', url='https://t.me/bitrix24_test_tolamiron_bot')))
                        # bot.send_message(message.chat.id, 'Введите текст сообщения для оператора поддержки',
                        #                  reply_markup=types.ReplyKeyboardRemove())

        # @log_errors
        # @bot.message_handler(content_types=['text'], func=lambda message: get_state(message.chat.id) == 5)
        # def enter_to_bitrix_chat(message):
        #     bx24 = Bitrix24('https://b24-iqrh1t.bitrix24.ru/rest/1/dmmf56d1jmeh5wqe/')
        #     print('bx24 = ', bx24.callMethod('crm.product.list'))
        #     # print(message.text)
        #     set_state(message.chat.id, 0)
        #     bot.send_message(message.chat.id, 'ok')

        @log_errors
        @bot.message_handler(content_types=['text'], func=lambda message: get_state(message.chat.id) == 4)
        def enter_text_to_appeal(message):
            if message.content_type == 'text':
                set_state(message.chat.id, 0)
                result = bot.get_user_profile_photos(message.chat.id, offset=1, limit=1)
                # print(result)
                photos = result.photos
                # print(photos)
                Path(os.path.join(settings.BASE_DIR, 'media') + f'/{message.chat.id}/avatar/').mkdir(parents=True,
                                                                                                     exist_ok=True)
                if photos:
                    avatar = max(photos[0], key=lambda x: x.width)
                    # file_id = avatar.file_id
                    downloaded_file = bot.download_file(bot.get_file(avatar.file_id).file_path)
                    src = f'media/{message.chat.id}/avatar/' + bot.get_file(
                        avatar.file_id).file_path.replace('photos/', '')
                    # print(src)
                    with open(src, 'wb') as new_file:
                        new_file.write(downloaded_file)
                    # bot.send_photo(message.chat.id, file_id, caption=file_id)
                    # bot.send_photo(message.chat.id, avatar)
                    newMessage = Message.objects.create(text=message.text)
                    newMessage.save()
                    # print(newMessage)
                    newChat, _ = Chat.objects.get_or_create(telegram_chat_id=message.chat.id,
                                                            username=message.from_user.username if message.from_user.username else 'Скрыт',
                                                            name=message.from_user.first_name,
                                                            avatar=f'{message.chat.id}/avatar/' + bot.get_file(
                                                                avatar.file_id).file_path.replace('photos/', ''))
                    # print(_)
                    if not _:
                        newChat = Chat.objects.get(telegram_chat_id=message.chat.id)
                        newChat.messages.add(newMessage)

                        newChat.save()
                    else:
                        newChat.messages.add(newMessage)

                        newChat.save()
                    # print(newChat)
                else:
                    newMessage = Message.objects.create(id=message.message_id, text=message.text,
                                                        time=datetime.datetime.now())
                    newMessage.save()
                    # print(newMessage)
                    newChat, _ = Chat.objects.get_or_create(telegram_chat_id=message.chat.id,
                                                            username=message.from_user.username if message.from_user.username else 'Скрыт',
                                                            name=message.from_user.first_name)
                    # print(_)
                    if not _:
                        newChat = Chat.objects.get(telegram_chat_id=message.chat.id)
                        newChat.messages.add(newMessage)

                        newChat.save()
                    else:
                        newChat.messages.add(newMessage)

                        newChat.save()
                    # print(newChat)

        @log_errors
        @bot.message_handler(content_types=['text'], func=lambda message: get_state(message.chat.id) == 1)
        def enter_text_to_send(message):
            # print(message.content_type)
            # print(message.content_type)
            # print(message.content_type == 'text')
            if message.content_type == 'text':
                # print(message.text)
                NewMail['text'] = message.text
                set_state(message.chat.id, 2)
                bot.send_message(message.chat.id, "Прикрепите изображение")
            else:
                bot.send_message(message.chat.id, "Введите текст рассылки")

        @log_errors
        @bot.message_handler(content_types=['photo'], func=lambda message: get_state(message.chat.id) == 2)
        def enter_photo(message):
            # print(message.content_type == 'text')
            # print(message.text)
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
                # print(NewMail['photo'])
                all_ok_markup = types.InlineKeyboardMarkup()
                all_ok_markup.row(types.InlineKeyboardButton("Подтвердить", callback_data="yes_all_ok"))
                bot.send_photo(message.chat.id, downloaded_file, caption=NewMail['text'], reply_markup=all_ok_markup)
            else:
                bot.send_message(message.chat.id, "Прикрепите изображение")

        @log_errors
        @bot.message_handler(content_types=['text'], func=lambda message: get_state(message.chat.id) == 3)
        def enter_auditory(message):
            # print(message.content_type == 'text')
            if message.content_type == 'text':
                # print(message.text)
                NewMail['auditory'] = message.text
                mail_to_db = Mail.objects.create(text=NewMail['text'], photo=NewMail['photo'],
                                                 auditory=NewMail['auditory'])
                # print(mail_to_db)
                mail_to_db.save()
                set_state(message.chat.id, 0)
                bot.send_message(message.chat.id, "Отлично. Ваша заявка принята")
            else:
                bot.send_message(message.chat.id, "Опишите целевую аудиторию для отправки email-рассылки")

        bot.set_update_listener(main_bot)

        @log_errors
        @bot.callback_query_handler(func=lambda call: True)
        def callback_answer(call):
            if call.data == "yes_all_ok":
                # print(call.message.text)
                set_state(call.message.chat.id, 3)
                bot.send_message(call.message.chat.id, "Опишите целевую аудиторию для отправки email-рассылки")
            else:
                # print(call.data)
                answer = Faq.objects.get(question=call.data)
                bot.send_message(call.message.chat.id, answer.answer)

        try:
            bot.polling(non_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)
            bot.polling(non_stop=True)
