from api.messages import COSUMER_SUPPORT_ALREADY_EXIST
from rest_framework import status
from v1.consumer.serializers.consumer_sub_category import ConsumerSubCategoryListSerializer
from v1.consumer.serializers.consumer_category import ConsumerCategoryListSerializer
from v1.commonapp.serializers.city import CityListSerializer
from v1.consumer.models.consumer_support import ConsumerSupport as ConsumerSupportTbl
from rest_framework import serializers
from v1.commonapp.views.custom_exception import CustomAPIException
from django.db import transaction
from datetime import datetime

from v1.consumer.views.common_functions import set_consumer_support_validated_data


class ConsumerSupportListSerializer(serializers.ModelSerializer):
    city = CityListSerializer(source='get_city')

    class Meta:
        model = ConsumerSupportTbl
        fields = ('name', 'id_string', 'email_id', 'phone_no', 'description', 'city', 'created_date', 'is_active', 'created_by')


class ConsumerSupportViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ConsumerSupportTbl
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'created_date')


class ConsumerSupportSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)
    city_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = ConsumerSupportTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_consumer_support_validated_data(validated_data)
            if ConsumerSupportTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                                 utility_id=validated_data['utility_id'],city_id=validated_data['city_id']).exists():
                raise CustomAPIException(COSUMER_SUPPORT_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                consumer_support_obj = super(ConsumerSupportSerializer, self).create(validated_data)
                consumer_support_obj.created_by = user.id
                consumer_support_obj.save()
                return consumer_support_obj

    def update(self, instance, validated_data, user):
        validated_data = set_consumer_support_validated_data(validated_data)
        if ConsumerSupportTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                             utility_id=validated_data['utility_id'],
                                             city_id=validated_data['city_id']).exists():
            raise CustomAPIException(COSUMER_SUPPORT_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                consumer_support_obj = super(ConsumerSupportSerializer, self).update(instance, validated_data)
                consumer_support_obj.updated_by = user.id
                consumer_support_obj.updated_date = datetime.utcnow()
                consumer_support_obj.save()
                return consumer_support_obj
