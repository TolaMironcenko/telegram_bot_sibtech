from rest_framework import serializers
from .models import Message, Chat


class ChatSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Chat
        fields = ('id', 'telegram_chat_id', 'username', 'name', 'avatar', 'messages')


class MessageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'text')
