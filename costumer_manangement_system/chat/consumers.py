from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from .models import ChatGroup, GroupMessage
import json
from asgiref.sync import async_to_sync

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        #scope delivers the same sort of information request does, but within the websocket
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        #bereinigt von leerzeichen im namen
        self.chatroom_name = self.chatroom_name.strip()
        self.chatroom= get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        
        if self.channel_layer is None:
            print("Channel layer not initialized")
            self.close()
            return #Early Exit

        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )

        #add and update online users
        if self.user not in self.chatroom.user_online.all():
            self.chatroom.user_online.add(self.user)
            self.update_online_count()
        
        self.accept()
    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )
        #add and update online users
        if self.user in self.chatroom.user_online.all():
            self.chatroom.user_online.remove(self.user)
            self.update_online_count()
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['message']

        message = GroupMessage.objects.create(
            body=body,
            author = self.user,
            group=self.chatroom
        )

        event = {
            'type':'message_handler',
            'message_id': message.id
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )
        
    def message_handler(self, event):
        message_id=event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user
        }
        html = render_to_string('chat/partials/chat_message_p.html', context=context)

        # HTML an den WebSocket senden
        self.send(text_data=json.dumps({
            'message_html': html
        }))

    def update_online_count(self):
        online_count = self.chatroom.user_online.count() - 1
        event={
            'type': 'online_count_handler',
            'online_count': online_count
        }
        async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)

    def online_count_handler(self, event):
        online_count = event['online_count']
        html = render_to_string("chat/partials/online_count.html", {'online_count': online_count})
        #HTML an das Websocket senden
        self.send(text_data=json.dumps({
            'online_count_html': html
        }))