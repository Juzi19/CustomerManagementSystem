from django.urls import path
from . import views

#Handles the URLs within the app

#paths
urlpatterns = [
    path('', views.start, name='file-start'),
    path('publicfiles/', views.publicfiles, name='files-public'),
    path('addafile/', views.add_a_file, name='files-add'),
    path('file/<int:fileid>', views.show, name='files-show'),
    path('filesinproject/<int:projectid>', views.projectshow, name='file-projectshow'),
    path('delete/<int:fileid>', views.delete, name='file-delete')
]