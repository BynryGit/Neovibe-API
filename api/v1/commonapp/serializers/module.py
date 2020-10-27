__author__ = "Arpita"

from rest_framework import serializers
from v1.commonapp.models.module import Module


class ModuleShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id_string', 'name')


class ModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = ('name', 'id_string')