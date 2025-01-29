from django.urls import path
from . import views

#Handles the URLs within the app

app_name = 'chat'

#paths
urlpatterns = [
    path('', views.chat_view, name='chat-start'),
    path('<username>/', views.get_or_createchatroom, name="start-chat"),
    path('room/<chatroom_name>/', views.chat_view, name="chatroom"),
    path('fileupload/<chatroom_name>/', views.chat_file_upload, name="chat-file-upload"),
    path('start/overview', views.chat, name='chat'),
    path('newchat/selecteduser', views.newchat_userinput, name='new-chat-userinput')
]