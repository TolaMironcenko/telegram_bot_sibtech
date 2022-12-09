from rest_framework import routers
from django.urls import path, include
from .views import MessageViewset, ChatViewet

router = routers.DefaultRouter()

router.register(r'messages', MessageViewset)
router.register(r'chats', ChatViewet)

urlpatterns = [

]

urlpatterns += router.urls
