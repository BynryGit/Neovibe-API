from api.messages import COSUMER_SUBCATEGORY_ALREADY_EXIST
from rest_framework import status
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string, \
    ConsumerCategory as ConsumerSubCategoryTbl
from v1.consumer.serializers.consumer_category import ConsumerCategoryListSerializer
from v1.consumer.models.consumer_sub_category import ConsumerSubCategory as ConsumerSubCategoryTbl
from rest_framework import serializers
from v1.commonapp.views.custom_exception import CustomAPIException
from django.db import transaction
from datetime import datetime

from v1.consumer.views.common_functions import set_consumer_subcategory_validated_data


class ConsumerSubCategoryListSerializer(serializers.ModelSerializer):
    consumer_category = ConsumerCategoryListSerializer(source='get_category_type')
    is_active = serializers.SerializerMethodField(method_name='conversion_bool')

    class Meta:
        model = ConsumerSubCategoryTbl
        fields = ('name', 'id_string', 'consumer_category', 'created_date', 'is_active', 'created_by')

    def conversion_bool(self, instance):
        if instance.is_active == True:
            return "Yes"
        else:
            return "No"


class ConsumerSubCategoryViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ConsumerSubCategoryTbl
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'created_date')


class ConsumerSubCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)
    category_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = ConsumerSubCategoryTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_consumer_subcategory_validated_data(validated_data)
            if ConsumerSubCategoryTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                                     utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(COSUMER_SUBCATEGORY_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                consumer_subcategory_obj = super(ConsumerSubCategorySerializer, self).create(validated_data)
                consumer_subcategory_obj.created_by = user.id
                consumer_subcategory_obj.updated_by = user.id
                consumer_subcategory_obj.save()
                return consumer_subcategory_obj

    def update(self, instance, validated_data, user):
        validated_data = set_consumer_subcategory_validated_data(validated_data)
        with transaction.atomic():
            consumer_subcategory_obj = super(ConsumerSubCategorySerializer, self).update(instance, validated_data)
            consumer_subcategory_obj.updated_by = user.id
            consumer_subcategory_obj.updated_date = datetime.utcnow()
            consumer_subcategory_obj.save()
            return consumer_subcategory_obj
