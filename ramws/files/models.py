from django.conf import settings
from django.db import models, transaction
from django.db.models.fields import CharField

from core.base import BaseModel

from .storage import Storage
from .queue import Queue


class Program(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name


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
        storage = Storage()
        return storage.open(name=self.input_path)

    @input_file.setter
    def input_file(self, value):
        self.input_path = f"{self.pk.hex}/input.zip"
        self.output_path = f"{self.pk.hex}/output.zip"

        self._input_file = value
        self.input_name = value.name

    @property
    def output_file(self):
        storage = Storage()
        return storage.open(name=self.output_path)

    @transaction.atomic
    def save(self, *args, **kwargs):
        storage = Storage()
        storage.save(name=self.input_path, content=self._input_file)

        queue = Queue()
        queue.post_run(run_id=self.id, program_name=self.program.code)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.input_name
