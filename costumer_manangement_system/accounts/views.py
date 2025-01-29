from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser


# Create your views here.

def homepage(request):
    return render(request, 'accounts/homepage.html', {"logged_in": False})

#if user is logged in
@login_required
def start(request):
    return render(request, 'accounts/start.html')

@login_required
def profile(request, username):
    if request.user.username == username:
        return render(request, 'accounts/profile.html')
    else:
        user = CustomUser.objects.get(username = username)
        return render(request, 'accounts/about.html', context={'aboutuser': user})

@login_required
def manageprofile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        description = request.POST.get('description')
        profile_photo = request.FILES.get('profile_photo')

        # Hier kannst du die Daten verarbeiten, z.B. den Benutzer aktualisieren
        user = request.user
        user.username = username
        user.email = email
        user.description = description
        if profile_photo:
            user.profile_photo = profile_photo
            print("Profile photo added")
        user.save()  # Speichern der Änderungen

        # Feedback-Nachricht hinzufügen
        messages.success(request, 'Deine Daten wurden erfolgreich aktualisiert!')

        return redirect('account-profile', username = request.user.username)  # Weiterleiten nach dem Speichern
    return render(request, 'accounts/editprofile.html')