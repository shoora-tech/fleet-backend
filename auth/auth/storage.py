from uuid import uuid4


def get_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"{uuid4()}.{ext}"