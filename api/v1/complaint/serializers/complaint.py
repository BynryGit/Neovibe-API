from datetime import datetime
from v1.complaint.serializers.complaint_subtype import ComplaintSubTypeListSerializer
from v1.complaint.serializers.complaint_type import ComplaintTypeListSerializer
from django.db import transaction
from rest_framework import serializers, status

from api.messages import CONSUMER_COMPLAINT_ALREADY_EXISTS
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.complaint.models.complaint import Complaint
from v1.complaint.views.common_functions import set_complaint_validated_data, generate_complaint_no
from v1.consumer.serializers.consumer_service_contract_details import ConsumerServiceContractDetailViewSerializer
from v1.registration.serializers.registration import ChoiceField

class ComplaintListSerializer(serializers.ModelSerializer):
    consumer_service_contract_detail_id=ConsumerServiceContractDetailViewSerializer(source='get_consumer_service_contract_detail_id')
    state = ChoiceField(choices=Complaint.CHOICES)
    complaint_sub_type = ComplaintSubTypeListSerializer(source='get_complaint_sub_type')
    class Meta:
        model = Complaint
        fields = ('complaint_name', 'id_string', 'created_by', 'state', 'consumer_service_contract_detail_id','consumer_no', 'complaint_no', 'created_date', 'is_active', 'complaint_sub_type')


class ComplaintViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = Complaint
        fields = '__all__'


class ComplaintSerializer(serializers.ModelSerializer):
    consumer_complaint_master_id = serializers.CharField(required=False, max_length=200)
    complaint_type_id = serializers.CharField(required=False, max_length=200)
    complaint_sub_type_id = serializers.CharField(required=False, max_length=200)
    complaint_status_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = Complaint
        fields = '__all__'

    def create(self, validated_data, consumer, user):
        validated_data = set_complaint_validated_data(validated_data)
        if Complaint.objects.filter(consumer_no=consumer.consumer_no, is_active=True,
                                    consumer_complaint_master_id=validated_data['consumer_complaint_master_id']).exists():
            raise CustomAPIException(CONSUMER_COMPLAINT_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                complaint = super(ComplaintSerializer, self).create(validated_data)
                complaint.tenant = consumer.tenant
                complaint.utility = consumer.utility
                complaint.created_by = user.id
                complaint.created_date = datetime.utcnow()
                complaint.complaint_no = generate_complaint_no(complaint)
                complaint.is_active = True
                complaint.save()
            return complaint

    def update(self, instance, validated_data, user):
        validated_data = set_complaint_validated_data(validated_data)
        with transaction.atomic():
            complaint = super(ComplaintSerializer, self).update(instance, validated_data)
            complaint.updated_by = user.id
            complaint.updated_date = datetime.utcnow()
            complaint.save()
            return complaint
