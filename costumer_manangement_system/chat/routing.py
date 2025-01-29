from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    #GANZ WICHTIG: <chatroom_name>/ !!!!falsch
    path("ws/chatroom/<chatroom_name>", ChatroomConsumer.as_asgi())
]