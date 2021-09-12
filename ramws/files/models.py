from django.conf import settings
from django.db import models, transaction

from core.base import BaseModel

from .queue import Queue
from .storage import Storage


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

    created_by = models.ForeignKey(
        to="accounts.User", on_delete=models.PROTECT, related_name="runs"
    )

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
    def input_path(self):
        return f"{self.hex_id}/input.zip"

    @property
    def output_path(self):
        return f"{self.hex_id}/output.zip"

    @property
    def logs_path(self):
        return f"{self.hex_id}/logs.txt"

    @property
    def warnings_path(self):
        return f"{self.hex_id}/warnings.txt"

    @property
    def input_file(self):
        storage = Storage()
        return storage.open(name=self.input_path)

    @input_file.setter
    def input_file(self, value):
        self.input_path = f"{self.hex_id}/input.zip"
        self.output_path = f"{self.hex_id}/output.zip"

        self._input_file = value
        self.input_name = value.name

    @property
    def output_file(self):
        storage = Storage()
        return storage.open(name=self.output_path)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self._state.adding:
            storage = Storage()
            storage.save(name=self.input_path, content=self._input_file)

            queue = Queue()
            queue.post_run(run_id=self.hex_id, program_name=self.program.code)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.input_name
