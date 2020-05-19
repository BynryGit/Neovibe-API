__author__ = "Priyanka"

from datetime import datetime
from django.db import transaction
from rest_framework import serializers
from v1.survey.models.survey_consumer import SurveyConsumer
from v1.survey.models.survey import Survey
from v1.supplier.models.supplier_master import SupplierMaster
from v1.survey.views.common_functions import set_survey_validate_data

class SurveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('id_string','name')

class vendorSerializers(serializers.ModelSerializer):
    class Meta:
        model = SupplierMaster
        fields = ('id_string','name')



class ConsumerViewSerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    survey_id = SurveSerializers(many=False, required=True,source='get_survey')
    vendor_id = vendorSerializers(many=False, required=True,source='get_vendor')

    class Meta:
        model = SurveyConsumer
        fields = ('id_string','tenant_name','consumer_no', 'first_name', 'middle_name', 'last_name', 'email_id', 'phone_mobile',
                  'address_line_1','survey_id','vendor_id')



class ConsumerSerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.name')
    survey_id = serializers.CharField(required=False, max_length=200)
    vendor_id = serializers.CharField(required=False, max_length=200)
    consumer_no = serializers.CharField(required=False, max_length=200)
    first_name = serializers.CharField(required=False, max_length=200)
    middle_name = serializers.CharField(required=False, max_length=200)
    last_name = serializers.CharField(required=False, max_length=200)
    email_id = serializers.CharField(required=False, max_length=200)
    phone_mobile = serializers.CharField(required=False, max_length=200)
    address_line_1 = serializers.CharField(required=False, max_length=200)
    zipcode = serializers.CharField(required=False, max_length=200)
    area_id = serializers.CharField(required=False, max_length=200)
    sub_area_id = serializers.CharField(required=False, max_length=200)
    category_id = serializers.CharField(required=False, max_length=200)
    sub_category_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = SurveyConsumer
        fields = ('__all__')

    def create(self, validated_data, user,survey):
        validated_data = set_survey_validate_data(validated_data)
        with transaction.atomic():
            survey_obj = super(ConsumerSerializer, self).create(validated_data)
            survey_obj.survey_id = survey.id
            survey_obj.created_by = user.id
            survey_obj.created_date = datetime.now()
            survey_obj.tenant = user.tenant
            survey_obj.utility = user.utility
            survey_obj.save()
            return survey_obj

    def update(self, instance, validated_data, user):
        validated_data = set_survey_validate_data(validated_data)
        with transaction.atomic():
            survey_obj = super(ConsumerSerializer, self).update(instance, validated_data)
            survey_obj.updated_by = user.id
            survey_obj.updated_date = datetime.now()
            survey_obj.save()
            return survey_obj

