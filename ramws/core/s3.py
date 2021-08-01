from django.conf import settings

import boto3


def get_service_resource():
    kwargs = dict(service_name="s3", region_name=settings.AWS_REGION)

    if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
        kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY

    return boto3.resource(**kwargs)


def get_bucket():
    s3 = get_service_resource()
    return s3.Bucket(name=settings.RUNS_S3_BUCKET)


def upload_file(bucket, path, data):
    path = settings.STORAGE_PERSONAL_FOLDER + path
    return bucket.put_object(Key=path, Body=data)


def download_file(bucket, path):
    path = settings.STORAGE_PERSONAL_FOLDER + path
    return bucket.get_object(Key=path)
