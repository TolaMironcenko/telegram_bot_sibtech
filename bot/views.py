from django.shortcuts import render
from .management.commands.bot import bot
from .models import Message, Chat
from .serilizers import MessageSerializer, ChatSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class MessageViewset(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ChatViewet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


# @api_view(['GET'])
# def get_messages(chat_id):
#     try:
#         Messages = Chat.objects.all()
#     except Exception as e:
#         print(str(e))
#         return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     serializer = ChatSerializer(allchats)
#     return Response(serializer.data)

#     print(allchats)


