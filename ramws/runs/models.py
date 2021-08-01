from django.db import models

from core.base import BaseModel


class Run(BaseModel):
    program = models.CharField(max_length=100)

    input_path = models.CharField(unique=True, max_length=200)
    output_path = models.CharField(unique=True, max_length=200)

    class Status(models.IntegerChoices):
        WARNING = 1
        OK = 2
        PENDING = 3
        CLIENT_ERROR = 4
        SERVER_ERROR = 5

    status = models.PositiveSmallIntegerField(choices=Status.choices)
