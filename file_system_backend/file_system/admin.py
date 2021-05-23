from django.contrib import admin
from file_system.models import *

class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'directory', 'create_at')

class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'directory', 'create_at')

# Register your models here.
admin.site.register(Folder ,FolderAdmin)
admin.site.register(File, FileAdmin)