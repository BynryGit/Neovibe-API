__author__ = "Arpita"

from rest_framework import serializers

from v1.commonapp.models.sub_module import SubModule
from v1.commonapp.serializers.module import ModuleSerializer


class SubModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubModule
        fields = ('name', 'id_string')


class SubModuleListSerializer(serializers.ModelSerializer):
    module = ModuleSerializer(many=False, required=True, source='get_module')

    class Meta:
        model = SubModule
        fields = ('id_string', 'module', 'name', 'is_active')


class SubModuleViewSerializer(serializers.ModelSerializer):
    module = ModuleSerializer(many=False, required=True, source='get_module')

    class Meta:
        model = SubModule
        fields = ('id_string', 'module', 'name', 'is_active')
