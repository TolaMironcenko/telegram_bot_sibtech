from django.shortcuts import render
from .management.commands.bot import bot
from .models import Message, Chat
from .serilizers import MessageSerializer, ChatSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import datetime


class MessageViewset(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ChatViewet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


@api_view(['POST'])
def send_to_telegram(request):
    request_body = json.loads(request.body)
    try:
        nowchat = Chat.objects.filter(telegram_chat_id=request_body['chat_id'])
    except Chat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    new_message = Message.objects.create(text=request_body['message'], from_user='admin', time=datetime.datetime.now())
    new_message.save()

    nowchat[0].messages.add(new_message)
    nowchat[0].save()
    # print(request_body['chat_id'])
    bot.send_message(request_body['chat_id'], request_body['message'])

    return Response("{\"OK\":\"true\"}")

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


