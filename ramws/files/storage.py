from django.conf import settings

from storages.backends.s3boto3 import S3Boto3Storage


class Storage(S3Boto3Storage):
    bucket_name = settings.RUNS_S3_BUCKET
