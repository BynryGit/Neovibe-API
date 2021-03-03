from rest_framework import serializers, status
from v1.complaint.models.consumer_complaint_master import ConsumerComplaintMaster as ConsumerComplaintMasterTbl
from v1.complaint.serializers.complaint_subtype import ComplaintSubTypeListSerializer
from datetime import datetime
from django.db import transaction
from api.messages import COMPLAINT_MASTER_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.complaint.views.common_functions import set_complaint_master_validated_data


class ConsumerComplaintMasterListSerializer(serializers.ModelSerializer):
    complaint_sub_type = ComplaintSubTypeListSerializer(source='get_complaint_sub_type')
    
    class Meta:
        model = ConsumerComplaintMasterTbl
        fields = ('id_string', 'name', 'complaint_sub_type','service_obj')


class ConsumerComplaintMasterViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ConsumerComplaintMasterTbl
        fields = (
            'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'id_string')


class ConsumerComplaintMasterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    complaint_type_id = serializers.CharField(required=False, max_length=200)
    complaint_sub_type_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ConsumerComplaintMasterTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_complaint_master_validated_data(validated_data)
            if ConsumerComplaintMasterTbl.objects.filter(name=validated_data['name'],
                                                         tenant_id=validated_data['tenant_id'],
                                                         utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(COMPLAINT_MASTER_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                complaint_obj = super(ConsumerComplaintMasterSerializer, self).create(validated_data)
                complaint_obj.created_by = user.id
                complaint_obj.updated_by = user.id
                complaint_obj.save()
                return complaint_obj

    def update(self, instance, validated_data, user):
        validated_data = set_complaint_master_validated_data(validated_data)
        with transaction.atomic():
            complaint_obj = super(ConsumerComplaintMasterSerializer, self).update(instance, validated_data)
            complaint_obj.updated_by = user.id
            complaint_obj.updated_date = datetime.utcnow()
            complaint_obj.save()
            return complaint_obj
