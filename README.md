##Introduction
This documentation outlines the usage and functionality of a RESTful API service created using Django, including JWT token authentication. The API has two endpoints: upload-files/ and download-files/, which allow users to upload and download files respectively. The endpoints require JWT bearer token authentication, which can be obtained by calling the /token/ API.

##Getting Started
To use the API service, you will need to have the following tools installed on your machine:
Python 3.6 or later
Django 3.0 or later
Django REST framework
djangorestframework_simplejwt

##Authentication
The API uses JWT bearer token authentication to ensure secure access to the endpoints. To obtain a token, call the /token/ API with valid username and password credentials. The API will return a token in JSON format, which should be used to authenticate requests to the other endpoints.


##Token API
POST /token/
#Request Body
{
  "username": "your_username",
  "password": "your_password"
}
#Response Body

{
  "access": "<your_access_token>",
  "refresh": "<your_refresh_token>"
}


##API Endpoints
#Upload Files API
POST /upload-files/
Request Headers
Authorization: Bearer <your_access_token>
Request Body
file: The file to be uploaded.
uploaded_by: The name of the person who uploaded the file.
title: The title of the image.
Response Body
{
  "title": "<file_title>",
  "uploaded_by": "<uploader_name>",
  "file": "<file>"
}
Response Body
{
    "status_code": 200,
    "status_message": "SUCCESS"
}
Download Files API
GET /download-files/
Request Headers
Authorization: Bearer <your_access_token>
Response Body
{
    "status_code": 200,
    "files": {
        "Test Sample": "http://127.0.0.1:8000/files/image_3_pcc9048.png",
        "Doodle Image": "http://127.0.0.1:8000/files/doodleimg_new.jpg"
    },
    "status_message": "SUCCESS"
}

Conclusion
This API service provides secure endpoints for uploading and downloading files using JWT token authentication. To use the service, obtain a token by calling the /token/ API, and include the token in the Authorization header for subsequent requests to the other endpoints.
