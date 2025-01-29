from django.contrib import admin
from .models import Project



# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    model = Project
    # Defines displayed data
    list_display = ('projectname','projectid', 'projectinfo' )

admin.site.register(Project, ProjectAdmin)




