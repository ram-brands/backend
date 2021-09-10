from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction

from core.base import BaseModel


class UserManager(BaseUserManager):
    @transaction.atomic
    def create(self, **fields):
        password = fields.pop("password", None)
        user = super().create(**fields)

        if password is not None:
            user.set_password(password)
            user.save()

        return user

    def create_superuser(self, **fields):
        fields.setdefault("is_staff", True)
        fields.setdefault("is_superuser", True)

        return self.create(**fields)


class User(BaseModel, AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    username = None
    email = models.EmailField(unique=True, verbose_name="email address")

    authorized_programs = models.ManyToManyField(
        to="files.Program", blank=True, related_name="authorized_users"
    )

    objects = UserManager()

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save(*args, **kwargs)

    def restore(self, *args, **kwargs):
        self.is_active = True
        self.save(*args, **kwargs)

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    @property
    def full_name(self):
        name_components = filter(bool, [self.first_name, self.last_name])
        name = " ".join(name_components)
        return name

    @property
    def owners(self):
        return {self}

    def __str__(self):
        return self.email
