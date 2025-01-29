from django.urls import path
from . import views

#Handles the URLs within the app

#paths
urlpatterns = [
    path('', views.overview, name='project-overview'),
    path('<int:myprojectid>/', views.project_details, name='project-detail'),
    path('<int:myprojectid>/edit/', views.editproject, name='project-edit'),
    path('newproject/', views.newproject, name='project-new'),

    
]