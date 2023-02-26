from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from django.utils.encoding import smart_str


from file_upload_app.models import *
from file_upload_app.urls import *
from .utility import generate_file_access_token

import logging
import sys
import mimetypes
import os

logger = logging.getLogger(__name__)

def index(request):
    #return HttpResponse("Hey, welcome to the Rest <b>File Upload</b> Service.")
    response = HttpResponse()
    response.write("<h1>Welcome to our File Uploading Service App!</h1>")
    response.write("<p>With our app, you can easily upload, and download your files.</p>")
    return response


class UploadFileAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        try:
            data = request.data
            if 'file' in data and 'title' in data:
                file = data['file']
                title = data['title']
                try:
                    file_object = FileUpload.objects.create(uploaded_by=request.user,file=file,title=title)
                    response["status_code"] = 200
                    response["status_message"] = "SUCCESS"
                    logger.info("UploadFileAPI Success %s",str(response))
                    
                    return Response(data=response)
                except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        logger.error("UploadFileAPI Error %s at %s",str(e), str(exc_tb.tb_lineno))

                        response['status_message'] = "Internal Server error"
                        response["status_code"] = 500
                        return Response(data=response)
            else:
                response['status_code'] = 400
                response["status_message"] = "Invalid request packet"
                response['internal_message'] = "parameter missing in request packet"
                logger.info("UploadFileAPI Failed Invalid request packet. Please check logs for request response packets")
                
                return Response(data=response)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("UploadFileAPI Error %s at %s",str(e), str(exc_tb.tb_lineno))
            
            response['status_message'] = "Internal Server error"
            response['status_code'] = 500

            return Response(data=response)

UploadFile = UploadFileAPI.as_view()


class GetFileAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        response = {}
        response["status_code"] = 500
        try:
            file_object = FileUpload.objects.all()
            links = {}
            
            file_token = generate_file_access_token(request.user)
            
            try:
                file_token_obj = FileAccessToken.objects.get(user=request.user)
                file_token_obj.file_token = file_token
                file_token_obj.created_at = datetime.now()
                file_token_obj.save(update_fields=["file_token","created_at"])
                logger.info("GetFile updated file access token ")
            except:
                logger.info("GetFile created file access token ")
                file_token_obj = FileAccessToken.objects.create(user=request.user, file_token=file_token, created_at=datetime.now())
            
            for file in file_object:
                links[file.title] = settings.HOST_URL + '/download-file/'+ file_token +"/"+ str(file.file_key)
            response['files'] = links
            response["status_code"] = 200
            response["status_message"] = "SUCCESS"
            logger.info("UploadFileAPI Success %s",str(response))
            
            return Response(data=response)
        except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("UploadFileAPI Error %s at %s",str(e), str(exc_tb.tb_lineno))

                response['status_message'] = "Internal Server error"
                response["status_code"] = 500
                return Response(data=response)

GetFile = GetFileAPI.as_view()


def DownloadFile(request,file_access_token,file_key):
    response = {}
    response["status_code"] = 500
    try:
        file_access_token_obj = FileAccessToken.objects.get(file_token=file_access_token)
        
        if file_access_token_obj.is_token_expired():
            response['status_code'] = 401
            response['status_message'] = "Token has expired"
            logger.error("DownloadFile: token has expired")
            return HttpResponse('<h1 style="color:red;">You are not authorized.</h1>')
        
        try:
            file_obj = FileUpload.objects.get(file_key=file_key)
            
            path_to_file = file_obj.file.url
            filename = file_obj.file.name
            logger.info("DownloadFile: internal error %s",str(settings.BASE_DIR))
            path_to_file = str(settings.BASE_DIR) + str(path_to_file)
            
            
            mime_type, _ = mimetypes.guess_type(path_to_file)
            if os.path.exists(path_to_file):
                with open(path_to_file, 'rb') as file:
                    response = HttpResponse(
                        file.read(), status=200, content_type=mime_type)
                    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(
                        str(filename))
                    logger.info("DownloadFile: File downloaded")
                    return response
                

            logger.error("DownloadFile: internal error")
            return HttpResponse('<h1 style="color:red;">You are not authorized.</h1>')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            response['status_code'] = 404
            response['status_message'] = "File not found"
            logger.error("DownloadFile: file not found"+ str(e) + "at line no." + str(exc_tb.tb_lineno))
            return HttpResponse(status=404)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        response['status_code'] = 401
        response['status_message'] = "You are not authorized"
        logger.error("DownloadFile: token not found" + str(e) + "at line no." + str(exc_tb.tb_lineno))
        return HttpResponse('<h1 style="color:red;">You are not authorized.</h1>')
        