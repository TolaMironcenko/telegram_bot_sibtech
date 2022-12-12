from rest_framework import serializers
from .models import Message, Chat


class MessageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'text', 'from_user', 'time')


class ChatSerializer(serializers.HyperlinkedModelSerializer):
    messages = MessageSerializer(read_only=True, many=True)
    class Meta:
        model = Chat
        fields = ('id', 'telegram_chat_id', 'username', 'name', 'avatar', 'messages')
