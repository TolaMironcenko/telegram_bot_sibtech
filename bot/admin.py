from django.contrib import admin
from .models import Faq, Mail, Chat


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('text', 'photo', 'auditory')


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('telegram_chat_id', 'username', 'name', 'avatar')
