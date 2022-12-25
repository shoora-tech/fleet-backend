from uuid import uuid4
from storages.backends.s3boto3 import S3Boto3Storage


class DriverImageStorageS3(S3Boto3Storage):
    location = "drivers"


def get_image_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    return f"{uuid4()}.{ext}"
