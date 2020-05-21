__author__ = "Arpita"

from rest_framework import serializers

from v1.commonapp.models.document import Document
from v1.commonapp.models.notes import Notes
from v1.commonapp.serializers.module import ModuleSerializer
from v1.commonapp.serializers.service_type import ServiceTypeSerializer
from v1.commonapp.serializers.sub_module import SubModuleSerializer
from v1.tenant.serializers.tenant import TenantSerializer
from v1.userapp.serializers.user import UserSerializer, GetUserSerializer
from v1.utility.serializers.utility import UtilitySerializer


class NoteViewSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    module = ModuleSerializer(many=False, required=True, source='get_module')
    sub_module = SubModuleSerializer(many=False, required=True, source='get_sub_module')
    service_type = ServiceTypeSerializer(many=False, required=True, source='get_service_type')
    # identification = UserSerializer(many=False, required=True, source='get_user_identification')

    class Meta:
        model = Notes
        fields = ('id_string', 'tenant', 'utility', 'module', 'sub_module', 'service_type', 'note_name', 'note_color',
                  'note', 'is_active', 'created_date')


class NoteListSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    module = ModuleSerializer(many=False, required=True, source='get_module')
    sub_module = SubModuleSerializer(many=False, required=True, source='get_sub_module')
    service_type = ServiceTypeSerializer(many=False, required=True, source='get_service_type')
    identification = UserSerializer(many=False, required=True, source='get_user_identification')

    class Meta:
        model = Document
        fields = ('id_string', 'tenant', 'utility', 'module', 'sub_module', 'service_type', 'identification',
                  'note_name', 'note_color', 'note', 'status', 'is_active', 'created_by', 'created_date')


class NoteSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = Notes
        fields = ('id_string', 'tenant', 'utility', 'note_name', 'note_color', 'note', 'status',
                  'is_active', 'created_date')

    def create(self, validated_data, user):
        note = super(NoteSerializer, self).create(validated_data)
        note.created_by = user.id
        note.tenant = user.tenant
        note.utility = user.utility
        note.is_active = True
        note.save()
        return note