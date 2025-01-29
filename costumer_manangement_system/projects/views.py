from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from django.http import Http404
from accounts.models import CustomUser
from .models import Project
from django.contrib import messages
from django.db.models import Max
from chat.models import ChatGroup


# Create your views here.

@login_required
def overview(request):
    return render (request, 'projects/overview.html')

@login_required
def project_details(request, myprojectid):
    #Displayes the page only if the user staff at nofrog
    #if request.user.employee == False:
       # return Http404


    project = get_object_or_404(Project, projectid=myprojectid)



    if request.method == 'POST':
        messagetext = request.POST.get('newmessage')
        #additional data
        author = str(request.user)

        #counts the messages still in the chat to adda new
        #if there are no data, initialize an empty list
        if 'chat' not in project.projectinfo or not project.projectinfo['chat']:
            project.projectinfo['chat'] = []
        chat_data = project.projectinfo['chat']
        number_of_messages = len(chat_data)
        myid = number_of_messages + 1

        #Appends a new message to the json file
        #theres a more efficient way using the collections.deque lib
        chat_data.insert(0,[messagetext, author, myid])

        project.projectinfo["chat"] = chat_data

        project.save()

        return redirect('project-detail', myprojectid=myprojectid)  # oder der entsprechende URL-Name
    #giving context to the selected project
    return render(request, 'projects/project-detail.html', {'project': project})

@login_required
def editproject(request, myprojectid):
    if not request.user.employee:
        return Http404
    else:
        project = get_object_or_404(Project, projectid=myprojectid)

        #Database get call all users
        users = CustomUser.objects.all()
        #Gets the chat
        chat = ChatGroup.objects.get(group_name = project.projectname)


        if request.method == 'POST':
            projectname = request.POST.get('projectname')
            projectdescription = request.POST.get('projectdescription')
            members = project.projectinfo['member']
            chat_data = project.projectinfo['chat']
            removemembersid = []

            #ChatGroup Name ändern
            if projectname:
                chat.group_name = projectname
                chat.save()

            #if there are members to delete
            for member in project.projectinfo['member']:
                if request.POST.get(f'{member[0]}') == 'on':
                    removemembersid.append(member[0])
                    removeprojectfromuser(users, member[0],myprojectid, projectname)


            newmember = request.POST.get('newmember')
            deletechat = request.POST.get('projectchatdelete')
            progress = request.POST.get('projectprogress')

            #sorts out inactive users and adds new ones
            for removemember in removemembersid:
                for index in range(len(members)-1, -1, -1):  # iterate backwards
                    if members[index][0] == removemember:
                        #removes a member
                        members.pop(index)

            
            # Initializes the variables
            userid = None
            username = None
            userrights = None
            user = None


            #Adds member by newmemberid
            #If there is a member to be add
            if newmember != "" and newmember != None:
                for user in users:
                    if user.id == int(newmember):
                        userid = user.id
                        username = user.username
                        userrights = user.employee
                        user = user
                if userid == None:
                    raise ValueError("User is not defined")
                
                membertoadd = [userid, username, userrights]
                members.append(membertoadd)
                adduser(user, projectname,project.projectid)

            if deletechat == 'on':
                chat_data = []

                        

            #Adds the data to the model form
            project.projectname = projectname
            project.projectinfo['description'] = projectdescription
            project.projectinfo['member'] = members
            project.projectinfo['chat'] = chat_data
            project.projectinfo['progress'] = progress

            project.save()
            messages.success(request, 'Projekteinstellungen wurden erfolgreich geändert')

            return redirect('project-detail',myprojectid = myprojectid)

        return render(request, 'projects/editproject.html', {'project':project, 'users': users})


#Removes the project from the user
def removeprojectfromuser(users, user_id, projectid, name):
    # Iterate the users to find the matching project
    user = None
    for user in users:
        # Check if the user ID matches the desired user ID
        if user.id == user_id:
            user = user
            # Filter out the projects that do not match the given project ID
            user.active_projects['projects'] = [
                project for project in user.active_projects['projects'] if project['id'] != projectid
            ]
            user.save()  # Save changes to the user
    chat = ChatGroup.objects.get(group_name = name)
    chat.members.remove(user)

#Adds user to a chatgroup
def adduser(user, name, id):
    user.active_projects['projects'].append({"name": name, "id": id})
    user.save()
    
    chat, created = ChatGroup.objects.get_or_create(group_name=name, is_private=True)
    
    chat.members.add(user)


@login_required
def newproject(request):
    if not request.user.employee:
        return Http404
    else:
        if request.method == 'POST':
            projectname = request.POST.get('projectname')

            # defines a unique id
            latest_project_id = Project.objects.aggregate(Max('projectid'))['projectid__max']
            project_id = (latest_project_id or 0) + 1  # id is 1 if no project exists
            # Generates a new Project
            newproject = Project(projectname=projectname, projectid=project_id)
            #adds the creating user to the project
            adduser(request.user, projectname, project_id)
            newproject.save()

            newproject.projectinfo['member'].append([request.user.id, request.user.username, request.user.employee])
            newproject.save()


            messages.success(request, 'Projekt wurde erfolgreich erstellt')

            return redirect('project-detail', myprojectid=project_id)



    return render(request, 'projects/newproject.html')