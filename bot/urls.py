from rest_framework import routers
from django.urls import path, include
from .views import MessageViewset, ChatViewet, send_to_telegram

router = routers.DefaultRouter()

router.register(r'messages', MessageViewset)
router.register(r'chats', ChatViewet)

urlpatterns = [
    path('send_to_telegram/', send_to_telegram)
]

urlpatterns += router.urls
