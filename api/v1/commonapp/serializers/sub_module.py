__author__ = "Arpita"

from rest_framework import serializers

from v1.commonapp.models.sub_module import SubModule
from v1.commonapp.serializers.module import ModuleSerializer
# from v1.userapp.serializers.user import PrivilegeSerializer


class SubModuleShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubModule
        fields = ('id_string', 'name')


class SubModuleSerializer(serializers.ModelSerializer):
    # module = ModuleSerializer(many=False, required=True, source='get_module')

    class Meta:
        model = SubModule
        fields = ('id_string', 'name')


class SubModuleListSerializer(serializers.ModelSerializer):
    module = ModuleSerializer(many=False, required=True, source='get_module')

    class Meta:
        model = SubModule
        fields = ('__all__')


class SubModuleViewSerializer(serializers.ModelSerializer):
    module = ModuleSerializer(many=False, required=True, source='get_module')

    class Meta:
        model = SubModule
        fields = ('id_string', 'module', 'name', 'is_active')
