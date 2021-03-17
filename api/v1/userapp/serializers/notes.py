__author__ = "Arpita"

from datetime import datetime

from django.db import transaction
from rest_framework import serializers, status

from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.commonapp.models.document import Document
from v1.commonapp.models.notes import Notes
from v1.commonapp.serializers.module import ModuleSerializer
# from v1.commonapp.serializers.service_request_type import ServiceTypeListSerializer
from v1.commonapp.serializers.sub_module import SubModuleSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.userapp.serializers.user import UserSerializer
from v1.userapp.views.common_functions import set_note_validated_data
from v1.utility.serializers.utility import UtilitySerializer


class NoteViewSerializer(serializers.ModelSerializer):

    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    module = ModuleSerializer(many=False, required=True, source='get_module')
    sub_module = SubModuleSerializer(many=False, required=True, source='get_sub_module')
    # service_type = ServiceTypeListSerializer(many=False, required=True, source='get_service_type')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = Notes
        fields = ('id_string', 'note_name', 'note_color', 'note', 'created_date', 'updated_date', 'tenant', 'utility',
                  'module', 'sub_module')


class NoteSerializer(serializers.ModelSerializer):
    utility_id = serializers.CharField( required=True, max_length=200)
    module_id = serializers.CharField( required=True, max_length=200)
    sub_module_id = serializers.CharField(required=True, max_length=200)
    # service_type_id = serializers.CharField(required=True, max_length=200)
    identification_id = serializers.CharField(required=True, max_length=200)
    note_name = serializers.CharField(required=True, max_length=200)
    note_color = serializers.CharField(required=False, max_length=200)
    note = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = Notes
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_note_validated_data(validated_data)
        if Notes.objects.filter(note_name=validated_data['note_name'], is_active=True).exists():
            raise CustomAPIException("Note already exists for specified user!",
                                     status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                note_obj = super(NoteSerializer, self).create(validated_data)
                note_obj.created_by = user.id
                note_obj.created_date = datetime.utcnow()
                note_obj.tenant = user.tenant
                note_obj.is_active = True
                note_obj.save()
                return note_obj

    def update(self, instance, validated_data, user):
        validated_data = set_note_validated_data(validated_data)
        if Notes.objects.filter(note_name=validated_data['note_name'], is_active=True).exists():
            raise CustomAPIException("Note already exists for specified user!",
                                     status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                note_obj = super(NoteSerializer, self).update(instance, validated_data)
                note_obj.updated_by = user.id
                note_obj.updated_date = datetime.utcnow()
                note_obj.is_active = True
                note_obj.save()
                return note_obj


class NoteListSerializer(serializers.ModelSerializer):

    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    module = ModuleSerializer(many=False, required=True, source='get_module')
    sub_module = SubModuleSerializer(many=False, required=True, source='get_sub_module')
    # service_type = ServiceTypeListSerializer(many=False, required=True, source='get_service_type')
    identification = UserSerializer(many=False, required=True, source='get_user_identification')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = Document
        fields = ('id_string', 'tenant', 'utility', 'module', 'sub_module', 'identification',
                  'note_name', 'note_color', 'note', 'status', 'created_date', 'updated_date')
