from django.contrib import admin
from .models import File

# Register your models here.

class FileAdmin(admin.ModelAdmin):
    model = File
    # Defines displayed data
    list_display = ('name','id', 'file', 'info' )

admin.site.register(File, FileAdmin)
