from datetime import datetime

from django.db import transaction
from rest_framework import serializers
from v1.consumer.models.consumer_complaints import ConsumerComplaints
from v1.consumer.views.common_functions import set_complaint_validated_data


class ComplaintListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsumerComplaints
        fields = ('complaint_name', 'id_string')


class ComplaintViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ConsumerComplaints
        fields = ('__all__')


class ComplaintSerializer(serializers.ModelSerializer):
    complaint_type_id = serializers.CharField(required=False, max_length=200)
    complaint_sub_type_id = serializers.CharField(required=False, max_length=200)
    complaint_status_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ConsumerComplaints
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_complaint_validated_data(validated_data)
        with transaction.atomic():
            complaint = super(ComplaintSerializer, self).create(validated_data)
            complaint.complaint_no = complaint.id
            complaint.created_by = user.id
            complaint.created_date = datetime.utcnow()
            complaint.tenant = user.tenant
            complaint.utility = user.utility
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