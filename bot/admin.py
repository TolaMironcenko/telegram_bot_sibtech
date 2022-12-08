from django.contrib import admin
from .models import Faq, Mail


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('text', 'photo', 'auditory')
