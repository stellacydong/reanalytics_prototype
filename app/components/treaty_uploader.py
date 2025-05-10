# app/components/treaty_uploader.py

import os
from django.conf import settings

def save_uploaded_file(uploaded_file):
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'treaties')
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, uploaded_file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    return file_path
