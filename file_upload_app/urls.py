from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path
# from django.conf.urls import url
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path(r'', views.index),
    path(r'token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'upload-file/', views.UploadFile, name="upload_file"),
    path(r'get-files/', views.GetFile, name="get_file"),
    re_path(r'download-file/(?P<file_access_token>[a-zA-Z0-9]+)/(?P<file_key>[a-zA-Z0-9-]+)/$', views.DownloadFile, name="download_file"),
]