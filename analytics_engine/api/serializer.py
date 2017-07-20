from django.conf.urls import url, include
from django.contrib.auth.models import User
from ae_reflex.models import *
from rest_framework import serializers
import json


class EventSerializer(serializers.HyperlinkedModelSerializer):
    source = serializers.ReadOnlyField(source='source_key.name')

    class Meta:
        model = Event
        fields = ('data', 'created', 'source')

    def get_data(self):
        return self.data
