from django.db import transaction
from rest_framework import serializers
from v1.commonapp.common_functions import set_note_validated_data
from v1.commonapp.models.notes import Notes
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.utility.serializers.utility import UtilitySerializer


class NoteListSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_tenant')

    class Meta:
        model = Notes
        fields = ('id_string', 'tenant', 'utility', 'note_name', 'note_color', 'note', 'created_date')


class NoteViewSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = Notes
        fields = ('id_string', 'tenant', 'utility', 'note_name', 'note', 'created_date')


class NoteSerializer(serializers.ModelSerializer):
    utility_id = serializers.CharField(required=False, max_length=200,
                                       error_messages={"required": "The field utility_id is required."})
    module_id = serializers.CharField(required=False, max_length=200,
                                      error_messages={"required": "The field module_id is required."})
    sub_module_id = serializers.CharField(required=False, max_length=200,
                                          error_messages={"required": "The field sub_module_id is required."})
    identification_id = serializers.CharField(required=False, max_length=200)
    note_name = serializers.CharField(required=True, max_length=200,
                                      error_messages={"required": "The field note_name is required."})
    note = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field note is required."})
    note_color = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = Notes
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_note_validated_data(validated_data)
        with transaction.atomic():
            note_obj = super(NoteSerializer, self).create(validated_data)
            note_obj.is_active = True
            note_obj.created_by = user.id
            note_obj.save()
            return note_obj

    def update(self, instance, validated_data, user):
        validated_data = set_note_validated_data(validated_data)
        with transaction.atomic():
            note_obj = super(NoteSerializer, self).update(instance, validated_data)
            note_obj.updated_by = user.id
            return note_obj
