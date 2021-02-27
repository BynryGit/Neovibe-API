__author__ = "chinmay"

from django.db import transaction
from django.utils import timezone
from api.messages import JOB_CARD_TEMPLATE_ALREADY_EXISTS
from rest_framework import serializers, status
from api.messages import *
from django.db import transaction
from v1.meter_data_management.models.job_card_template import \
    JobCardTemplate as JobCardTemplateTbl
from v1.meter_data_management.views.common_function import set_job_card_template_validated_data
from v1.commonapp.views.custom_exception import CustomAPIException
from datetime import datetime


class JobCardTemplateListSerializer(serializers.ModelSerializer):


    class Meta:
        model = JobCardTemplateTbl
        fields = ('task_name', 'id_string', 'created_date', 'is_active', 'created_by')


class JobCardTemplateViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = JobCardTemplateTbl
        fields = ('task_name', 'id_string', 'utility', 'utility_id_string', 'tenant', 'tenant_id_string')


class JobCardTemplateSerializer(serializers.ModelSerializer):
    meter_read_json_obj = serializers.JSONField(required=False)
    additional_parameter_json = serializers.JSONField(required=False)
    utility_id = serializers.UUIDField(required=False)
    tenant_id = serializers.UUIDField(required=False)
    task_name = serializers.CharField(required=True, max_length=200,
                                     error_messages={
                                         "required": "The field smart meter api name is required."})

    class Meta:
        model = JobCardTemplateTbl
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_job_card_template_validated_data(validated_data)
        if JobCardTemplateTbl.objects.filter(tenant_id=validated_data['tenant_id'],
                                             utility_id=validated_data['utility_id'],
                                             task_name=validated_data['task_name']).exists():
            raise CustomAPIException(JOB_CARD_TEMPLATE_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                job_card_template_obj = super(JobCardTemplateSerializer, self).create(validated_data)
                job_card_template_obj.tenant = user.tenant
                job_card_template_obj.created_by = user.id
                job_card_template_obj.save()
                return job_card_template_obj

    def update(self, instance, validated_data, user):
        validated_data = set_job_card_template_validated_data(validated_data)
        with transaction.atomic():
            job_card_template_obj = super(JobCardTemplateSerializer, self).update(instance, validated_data)
            job_card_template_obj.tenant = user.tenant
            job_card_template_obj.updated_by = user.id
            job_card_template_obj.updated_date = timezone.now()
            job_card_template_obj.save()
            return job_card_template_obj
