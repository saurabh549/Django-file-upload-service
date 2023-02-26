import hashlib
from datetime import datetime


def generate_file_access_token(user):
    timestamp = datetime.now()
    encoded_string = (str(user) + str(timestamp)).encode()
    return hashlib.md5(encoded_string).hexdigest()