from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Project(models.Model):

    projectname = models.CharField(max_length=150)
    projectid = models.IntegerField(default=0)
    projectinfo = models.JSONField(default=dict)

    def clean(self):
        try:
            # Validates the JSON Field
            data = self.projectinfo

            if 'description' not in data:
                raise ValidationError("Beschreibung fehlt")
            if 'member' not in data or not isinstance(data['member'], list):
                raise ValidationError("Member muss eine Liste sein.")
            if 'chat' not in data or not isinstance(data['chat'], list):
                raise ValidationError("Chat muss eine Liste sein.")
            if 'files' not in data or not isinstance(data['files'], list):
                raise ValidationError("Files muss eine Liste sein.")
            if 'progress' not in data:
                raise ValidationError("Fortschritt ist erforderlich.")
        except (ValueError, TypeError) as e:
            raise ValidationError(f"Ungültiges JSON-Format: {e}")

    def save(self, *args, **kwargs):
        #default values
        self.projectinfo.setdefault("member", [])
        self.projectinfo.setdefault("chat", [])
        self.projectinfo.setdefault("files", [])
        self.projectinfo.setdefault("description", "")
        self.projectinfo.setdefault("progress", "start")


        self.clean()  # Validates the form before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.projectinfo.get("name", "Unnamed Project")


"""
JSON Field example:

#before
"name": String,  #Defines the projects' name
"id": 1,    #Unique Project ID

#now json

{

    "description": String,    
    "member": [[uuid, status], [uuid, status]],  #UUID: every users' unique id (user.id), status: whether the user is employee or client
    "chat": [[message, author(uuid)],[message, author(uuid)]],  #Contains the Message and the messages author
    "files": [[fileid],[filename, path]],  #Gives information about files saved whithin the project
    "progress": "done" #Defines  the current state of the project(e.g production, testing, etc...)

}


### Clean:

{

    "description": String,    
    "member": [[uuid, name,  status], [uuid, name, status]],  
    "chat": [[message, author, 1],[message, author, id]],  
    "files": [[filename, path],[filename, path]],  
    "progress": "done" 

}

"""
