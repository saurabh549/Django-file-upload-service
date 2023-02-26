from django.db import models
from django.contrib.auth.models import User

from datetime import datetime, timedelta, timezone
import uuid

class FileUpload(models.Model):
    
    file_key = models.UUIDField(unique=True,primary_key=True,default=uuid.uuid4)
    
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    file = models.FileField(upload_to='')
    
    title = models.CharField(default="Null",max_length=500)
    
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "FileUpload"
        verbose_name_plural = "FileUpload"

    def __str__(self):
        return str(self.uploaded_by)
    
    
class FileAccessToken(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    file_token = models.CharField(max_length=200)
    
    created_at = models.DateTimeField(auto_now=False)
    
    def __str__(self) -> str:
        return self.user.username
    
    def is_token_expired(self) -> bool:
        expiration_time = FileUploadConfig.objects.all().first().file_access_token_expiration_time
        if self.created_at < datetime.now(timezone.utc) - timedelta(minutes=int(expiration_time)):
            return True
        return False


class FileUploadConfig(models.Model):
    
    file_access_token_expiration_time = models.IntegerField(default=5,help_text="File access token will get expired after the defined time in min.")
    
    def __str__(self) -> str:
        return "Config"