from rest_framework import serializers
from v1.complaint.models.complaint_type import ComplaintType as ComplaintTypeTbl
from v1.commonapp.views.settings_reader import SettingReader

setting_reader = SettingReader()
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import COMPLAINT_TYPE_ALREADY_EXIST
from v1.complaint.views.common_functions import set_complaint_type_validated_data
from v1.utility.serializers.utility_product import UtilityProductListSerializer
from rest_framework import status


class ComplaintTypeListSerializer(serializers.ModelSerializer):


    class Meta:
        model = ComplaintTypeTbl
        fields = ('name', 'id_string', 'created_date', 'is_active', 'created_by')


class ComplaintTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ComplaintTypeTbl
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'created_date')


class ComplaintTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)


    class Meta:
        model = ComplaintTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_complaint_type_validated_data(validated_data)
            if ComplaintTypeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                               utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(COMPLAINT_TYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                complaint_type_obj = super(ComplaintTypeSerializer, self).create(validated_data)
                complaint_type_obj.created_by = user.id
                complaint_type_obj.save()
                return complaint_type_obj

    def update(self, instance, validated_data, user):
        validated_data = set_complaint_type_validated_data(validated_data)
        if ComplaintTypeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                           utility_id=validated_data['utility_id']).exists():
            raise CustomAPIException(COMPLAINT_TYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                complaint_type_obj = super(ComplaintTypeSerializer, self).update(instance, validated_data)
                complaint_type_obj.updated_by = user.id
                complaint_type_obj.updated_date = datetime.utcnow()
                complaint_type_obj.save()
                return complaint_type_obj
