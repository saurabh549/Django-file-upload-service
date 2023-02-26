Introduction:
This documentation outlines the usage and functionality of a RESTful API
service created using Django, including JWT token authentication. The API has
two endpoints: upload-files/ and get-files/, which allow users to upload
and download files respectively. The endpoints require JWT bearer token
authentication, which can be obtained by calling the /token/ API.


you can set the time to expire the file link in FileUploadConfig model from django admin.

If you try to access the file with the link after the time you specified in the FileUploadConfig model , link will not work .

and you can't call the apis without passing the correct username and password. so it is a two layer security.



Steps to setup the Project on Local:

1. Take the Clone of the repository.

2. Open terminal

3. Create virtual environment by using the following command:
    python3 -m virtualenv venv -p python3

4. Activate venv by using the folllowing command:
    source venv/bin/activate

5. Go inside the project folder.

6. Install the dependencies by following command:
pip install requirment.txt

7. Run the following commands:

    python manage.py makemigrations

    python manage.py migrate

    settings.py DEBUG True

    python manage.py createsuperuser

    python manage.py runserver

8. Go to admin and create a object for FileUploadConfig , by default it will take the 5 minute as value.

9. Import Given Postman Collection in POSTMAN.

10. Set username and password in collection variables

11. call token generation API

12. call file upload API and upload a file

13. call get files API and you can download files directly clicking on the links you get in the response.
