from django.db import models
from django.contrib.auth.models import User
from django_pgjson.fields import JsonField, JsonBField
import string
from django.utils.crypto import get_random_string


class Project(models.Model):
    external_id = models.CharField(max_length=100, db_index=True, unique=True)
    name = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @staticmethod
    def create_project(name):
        external_id = get_random_string(length=24, allowed_chars=string.ascii_uppercase + string.digits)
        return Project.objects.create(name=name, external_id=external_id)


class Event(models.Model):
    project = models.ForeignKey("ae_reflex.Project", related_name='events')
    data = JsonBField()
    source_key = models.ForeignKey("ae_reflex.Key", null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project.name


class Key(models.Model):
    project = models.ForeignKey("ae_reflex.Project", related_name='keys')
    name = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=100)

    @staticmethod
    def create_key(name, project):
        key = get_random_string(length=24, allowed_chars=string.ascii_uppercase + string.digits)
        return Key.objects.create(name=name, unique_id=key, project=project)