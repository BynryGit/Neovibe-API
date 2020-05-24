__author__ = "Arpita"

from datetime import datetime

from django.db import transaction
from rest_framework import serializers

from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.models.document import Document
from v1.commonapp.models.notes import Notes
from v1.commonapp.serializers.module import ModuleSerializer
from v1.commonapp.serializers.service_type import ServiceTypeListSerializer
from v1.commonapp.serializers.sub_module import SubModuleSerializer
from v1.tenant.serializers.tenant import GetTenantSerializer
from v1.userapp.serializers.user import UserSerializer, GetUserSerializer
from v1.userapp.views.common_functions import set_note_validated_data
from v1.utility.serializers.utility import UtilitySerializer


class NoteViewSerializer(serializers.ModelSerializer):

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    module = ModuleSerializer(many=False, required=True, source='get_module')
    sub_module = SubModuleSerializer(many=False, required=True, source='get_sub_module')
    service_type = ServiceTypeListSerializer(many=False, required=True, source='get_service_type')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = Notes
        fields = ('id_string', 'tenant', 'utility', 'module', 'sub_module', 'service_type', 'note_name', 'note_color',
                  'note', 'is_active', 'created_date')


class NoteSerializer(serializers.ModelSerializer):
    module_id = serializers.CharField( required=False, max_length=200)
    sub_module_id = serializers.CharField(required=False, max_length=200)
    service_type_id = serializers.CharField(required=False, max_length=200)
    identification_id = serializers.CharField(required=False, max_length=200)
    note_name = serializers.CharField(required=False, max_length=200)
    note_color = serializers.CharField(required=False, max_length=200)
    note = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = Notes
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data =  set_note_validated_data(validated_data)
        with transaction.atomic():
            note_obj = super(NoteSerializer, self).create(validated_data)
            note_obj.created_by = user.id
            note_obj.tenant = user.tenant
            note_obj.utility = user.utility
            note_obj.is_active = True
            note_obj.save()
            return note_obj

    def update(self, instance, validated_data, user):
        validated_data = set_note_validated_data(validated_data)
        with transaction.atomic():
            note_obj = super(NoteSerializer, self).update(instance, validated_data)
            note_obj.updated_by = user.id
            note_obj.updated_date = datetime.utcnow()
            note_obj.is_active = True
            note_obj.save()
            return note_obj


class NoteListSerializer(serializers.ModelSerializer):

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    module = ModuleSerializer(many=False, required=True, source='get_module')
    sub_module = SubModuleSerializer(many=False, required=True, source='get_sub_module')
    service_type = ServiceTypeListSerializer(many=False, required=True, source='get_service_type')
    identification = UserSerializer(many=False, required=True, source='get_user_identification')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = Document
        fields = ('id_string', 'tenant', 'utility', 'module', 'sub_module', 'service_type', 'identification',
                  'note_name', 'note_color', 'note', 'status', 'is_active', 'created_date')
