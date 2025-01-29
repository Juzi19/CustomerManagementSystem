from django.db import models

# Create your models here.
class File (models.Model):
    name = models.CharField(max_length=100, default='NONE')
    file = models.FileField(upload_to='documents/', default='documents/default_file.txt')
    info = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        # Ensure the default structure for 'files'
        self.info.setdefault("in_projects", [])
        #[[projectname, projectid]]
        self.info.setdefault("author", "")
        self.info.setdefault("public", False)
        super().save(*args, **kwargs)

#Default setting for project doc

