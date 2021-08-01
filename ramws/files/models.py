from django.conf import settings
from django.db import models, transaction
from django.db.models.fields import CharField

from rest_framework.status import HTTP_200_OK

from core.base import BaseModel
from core.s3 import download_file, get_bucket, upload_file


class Program(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Run(BaseModel):
    input_name = models.CharField(max_length=200)

    program = models.ForeignKey(
        to="files.Program", on_delete=models.PROTECT, related_name="runs"
    )

    input_path = models.CharField(unique=True, max_length=200)
    output_path = models.CharField(unique=True, max_length=200)

    class Status(models.IntegerChoices):
        WARNING = 1
        OK = 2
        PENDING = 3
        CLIENT_ERROR = 4
        SERVER_ERROR = 5

    status = models.PositiveSmallIntegerField(
        choices=Status.choices, default=Status.PENDING
    )

    @property
    def input_file(self):
        bucket = get_bucket(name=settings.RUNS_S3_BUCKET)
        response = download_file(bucket=bucket, path=self.input_path)

        if response.status_code != HTTP_200_OK:
            raise Exception

        return response.content.read()

    @input_file.setter
    def input_file(self, value):
        self.input_path = f"{self.pk.hex}/input.zip"
        self.output_path = f"{self.pk.hex}/output.zip"

        self._input_content = value

    @property
    def output_file(self):
        bucket = get_bucket(name=settings.RUNS_S3_BUCKET)
        response = download_file(bucket=bucket, path=self.input_path)

        if response.status_code != HTTP_200_OK:
            raise Exception()

        return response.content.read()

    @transaction.atomic
    def save(self, *args, **kwargs):
        bucket = get_bucket(name=settings.RUNS_S3_BUCKET)
        response = upload_file(
            bucket=bucket, path=self.input_path, content=self._input_content
        )

        if response.status_code != HTTP_200_OK:
            raise Exception()

        super().save(*args, **kwargs)
