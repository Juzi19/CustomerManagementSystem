from django.urls import path
from . import views

#Handles the URLs within the app

#paths
urlpatterns = [
    path('', views.start, name='account-start'),
    path('profile/<username>/', views.profile, name='account-profile'),
    path('manageprofile', views.manageprofile, name='manageprofile')
]