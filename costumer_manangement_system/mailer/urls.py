from django.urls import path
from . import views

#Handles the URLs within the app
#paths
urlpatterns = [
    path('', views.announce, name='a-ment'),
]