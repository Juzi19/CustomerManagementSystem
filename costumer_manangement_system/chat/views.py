from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import ChatmessageCreateForm
from django.http import Http404, HttpResponse, HttpResponseForbidden
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.

@login_required
def chat_view(request, chatroom_name='public-chat'):
    chatroom_name = str(chatroom_name)
    chat_group, created = ChatGroup.objects.get_or_create(group_name=chatroom_name)
    chat_messages = chat_group.chat_message.all()[:30]
    form = ChatmessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            print("Fehler aufgrund mangelnder Zugriffsrechte")
            raise HttpResponseForbidden("Keine Zugriffsrechte")
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break

    if request.headers.get('HX-Request'):
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message': message,
                'user': request.user
            }
            return render(request, 'chat/partials/chat_message_p.html', context)
        
    context = {
        "chat_messages": chat_messages,
        "form": form, 
        "other_user": other_user,
        "chatroom_name": chatroom_name
    }
    return render(request, "chat/chat-home.html", context)

@login_required
def get_or_createchatroom(request, username):
    if request.user.username == username:
        return redirect('chat:chat-start')
    
    other_user = CustomUser.objects.get(username = username)
    my_private_chatrooms = request.user.chat_groups.filter(is_private=True)
    
    if my_private_chatrooms.exists():
        for chatroom in my_private_chatrooms:
            if other_user in chatroom.members.all():
                return redirect('chat:chatroom', chatroom_name = chatroom.group_name)
   
    chatroom = ChatGroup.objects.create( is_private = True )
    chatroom.members.add(other_user, request.user)   
    return redirect('chat:chatroom',chatroom_name = chatroom.group_name)

def chat_file_upload(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name = chatroom_name)

    if request.FILES:
        file = request.FILES['file']
        message = GroupMessage.objects.create(
            file = file,
            author = request.user,
            group = chat_group
        )

        channel_layer = get_channel_layer()
        event = {
            'type': 'message_handler',
            'message_id': message.id
        }
        async_to_sync(channel_layer.group_send)(
            chatroom_name, event
        )
    return HttpResponse()

@login_required
def chat(request):
    chats = ChatGroup.objects.filter(members = request.user)
    mychats = []
    for chat in chats:
        singlemembers = []
        members = CustomUser.objects.filter(chat_groups = chat)
        for member in members:
            if member == request.user:
                continue
            singlemembers.append(member.username)
        mychats.append([chat, singlemembers])
        

    return render(request, 'chat/chat.html', {"chats":mychats})

@login_required
def newchat_userinput(request):
    if request.method == 'POST':
        user = request.POST.get('username_chat')
        return redirect('chat:start-chat', username=user)
    return render(request, 'chat/create_new_chat.html')
