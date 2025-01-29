from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from accounts.models import CustomUser
from .models import Annoncement
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

@login_required
def announce(request):
    if not request.user.employee:
        return HttpResponseForbidden
    users = CustomUser.objects.all()
    if request.method == 'POST':
        name = request.POST.get('betreff')
        body = request.POST.get('text')
        users = CustomUser.objects.all()
        announcementmembers = []
        for user in users:
            if request.POST.get(f'{user.username}') == 'on':
                announcementmembers.append(user)
        
        new_announcement = Annoncement(name=name, body = body)
        new_announcement.save()

        new_announcement.members.set(announcementmembers)

        recipientemail = [user.email for user in announcementmembers]

        send_announcement_mail(name, f'Neue Ankündigung {body} ', recipientemail)

        messages.success(request, "Ankündigung erfolgreich an alle Benutzer verschickt")

        return redirect('/accounts')
    
    return render(request, 'mailer/announce.html', {"users": users})


def send_announcement_mail(subject, body, email:list):
    send_mail(
        subject, 
        body,
        settings.DEFAULT_FROM_EMAIL,
        email,
        fail_silently=False
    )
