from rest_framework import serializers
from v1.complaint.models.complaint_sub_type import ComplaintSubType as ComplaintSubTypeTbl
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import COMPLAINT_SUBTYPE_ALREADY_EXIST
from v1.complaint.views.common_functions import set_complaint_subtype_validated_data
from rest_framework import status
from v1.complaint.serializers.complaint_type import ComplaintTypeListSerializer


class ComplaintSubTypeListSerializer(serializers.ModelSerializer):
    complaint_type = ComplaintTypeListSerializer(source="get_complaint_type")

    class Meta:
        model = ComplaintSubTypeTbl
        fields = ('name', 'id_string', 'complaint_type', 'created_date', 'is_active', 'created_by')


class ComplaintSubTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ComplaintSubTypeTbl
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'created_date')


class ComplaintSubTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)
    complaint_type_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = ComplaintSubTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_complaint_subtype_validated_data(validated_data)
            if ComplaintSubTypeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                                  utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(COMPLAINT_SUBTYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                complaint_subtype_obj = super(ComplaintSubTypeSerializer, self).create(validated_data)
                complaint_subtype_obj.created_by = user.id
                complaint_subtype_obj.updated_by = user.id
                complaint_subtype_obj.save()
                return complaint_subtype_obj

    def update(self, instance, validated_data, user):
        validated_data = set_complaint_subtype_validated_data(validated_data)
        with transaction.atomic():
            complaint_subtype_obj = super(ComplaintSubTypeSerializer, self).update(instance, validated_data)
            complaint_subtype_obj.updated_by = user.id
            complaint_subtype_obj.updated_date = datetime.utcnow()
            complaint_subtype_obj.save()
            return complaint_subtype_obj
