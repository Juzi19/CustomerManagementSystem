from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from projects.models import Project
from .models import File
from django.contrib import messages
from django.http import FileResponse, HttpResponseForbidden, Http404, HttpResponseNotFound
import os
from django.conf import settings
from projects.models import Project

# Create your views here.
@login_required
def start(request):
    
    user = request.user

    files = File.objects.all()
    
    filesinuser = []


    projects = Project.objects.all()


    #Filters the user file in all files
    #Might be inefficients
    for userfile in user.files['id']:
        for file in files:
            if userfile == file.id:
                selected_projects = []
                for p in file.info['in_projects']:
                    for project in projects:
                        if project.projectid == int(p):
                            selected_projects.append(project)
                filesinuser.append([file, selected_projects])
    #giving context by an databse call to get all files from a user
    return render(request, 'documents/file-start.html', {'filesinuser': filesinuser} )

@login_required
def publicfiles (request):
    files = File.objects.all()
    publicfiles = []
    for file in files:
        if file.info['public']:
            publicfiles.append(file)
    return render(request, 'documents/file-public.html', {'publicfiles': publicfiles, 'title': 'NoFrog - öffentliche Dokumente'})

@login_required
def add_a_file(request):
    projects = Project.objects.all()

    if request.method == 'POST':
        file = request.FILES.get('file')
        author = request.user.username
        name = request.POST.get('name')
        public = request.POST.get('public')
        in_project = request.POST.get('in_project')


        if public == 'on':
            public = True
        else:
            public = False
        
        newfile = File(name=name)
        newfile.file = file
        newfile.info['author'] = author
        newfile.info['public'] = public
        newfile.info['in_projects'] = in_project
        newfile.save()
        user = request.user

        #Add the file to the user json
        user.files['id'].append(newfile.id)
        user.save()

        #Does not work
        if in_project != "---" or in_project!=None or in_project!="":
            #add the file to the project JSON
            for project in projects:
                if str(project.projectid) == str(in_project):
                    project.projectinfo['files'].append(newfile.id)
                    project.save()
        
   
        messages.success(request, 'Dokument wurde erfolgreich erstellt')

        return redirect('file-start')

    myprojects = []
    for project in projects:
        for member in project.projectinfo['member']:
            if member[0] == request.user.id:
                myprojects.append(project)
        

    return render(request, 'documents/add-file.html',{'projects': myprojects})

@login_required
def show(request, fileid):
    file = File.objects.get(id=fileid)

    if file.info["author"] == request.user.username or file.info["public"] or checkaccessviaproject(file, request.user):
         # Construct the full file path
        file_path = os.path.join(settings.MEDIA_ROOT, 'documents', file.file.path)

        # Check if file exists
        if not os.path.exists(file_path):
            raise Http404("File does not exist")
        return FileResponse(open(file_path, 'rb'))
    
    else:
        return HttpResponseForbidden("Du hast keine Zugriffsrechte auf das Dokument")
    
def checkaccessviaproject(file, user):
    for projectid in file.info["in_projects"]:
        for element in user.active_projects["projects"]:
            # Ensure each element is a dictionary with an 'id' key
            if isinstance(element, dict) and "id" in element:
                if element["id"] == projectid:
                    return True
    return False



@login_required
def projectshow(request, projectid):
    if not userinproject(request.user, projectid):
        return HttpResponseForbidden("Nicht ausreichende Zugriffsrechte")

    try:
        project = Project.objects.get(projectid=projectid)
    except Project.DoesNotExist:
        return HttpResponseNotFound("Project not found.")

    files = File.objects.all()
    files_inproject = []
    for file in files:
        if str(projectid) == file.info["in_projects"]:
            files_inproject.append(file)

    return render(request, 'documents/file-projectshow.html', {"files": files_inproject, "project": project})

#checks if the user is a project member
def userinproject(user, projectid):
    for element in user.active_projects["projects"]:
        # Ensure each element is a dictionary with an 'id' key
        if isinstance(element, dict) and "id" in element:
            if str(element["id"]) == str(projectid):
                return True
    return False

@login_required
def delete(request, fileid):
    file = File.objects.get(id = fileid)
    file.delete()
    messages.success(request, "Dokument erfolgreich gelöscht")
    return redirect('file-start')