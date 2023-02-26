from django.contrib import admin
from file_upload_app.models import *

# Register your models here.
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('uploaded_by', 'file', 'timestamp')
    readonly_fields = ('file_key',)

admin.site.register(FileUpload,FileUploadAdmin)
admin.site.register(FileAccessToken)
admin.site.register(FileUploadConfig)


