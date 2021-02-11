from rest_framework import serializers
from v1.consumer.models.consumer_category import ConsumerCategory as ConsumerCategoryTbl
from v1.commonapp.views.settings_reader import SettingReader

setting_reader = SettingReader()
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import COSUMER_CATEGORY_ALREADY_EXIST
from rest_framework import status
from v1.utility.serializers.utility_product import UtilityProductListSerializer
from v1.consumer.views.common_functions import set_consumer_category_validated_data


class ConsumerCategoryListSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField(method_name='conversion_bool')
    utility_product = UtilityProductListSerializer(source='get_utility_product')

    class Meta:
        model = ConsumerCategoryTbl
        fields = ('name', 'id_string', 'utility_product', 'created_date', 'is_active', 'created_by')

    def conversion_bool(self, instance):
        if instance.is_active == True:
            return "Yes"
        else:
            return "No"


class ConsumerCategoryViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ConsumerCategoryTbl
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'created_date')


class ConsumerCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)
    utility_product_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = ConsumerCategoryTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_consumer_category_validated_data(validated_data)
            if ConsumerCategoryTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                                  utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(COSUMER_CATEGORY_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                consumer_category_obj = super(ConsumerCategorySerializer, self).create(validated_data)
                consumer_category_obj.created_by = user.id
                consumer_category_obj.updated_by = user.id
                consumer_category_obj.save()
                return consumer_category_obj

    def update(self, instance, validated_data, user):
        validated_data = set_consumer_category_validated_data(validated_data)
        with transaction.atomic():
            consumer_category_obj = super(ConsumerCategorySerializer, self).update(instance, validated_data)
            consumer_category_obj.updated_by = user.id
            consumer_category_obj.updated_date = datetime.utcnow()
            consumer_category_obj.save()
            return consumer_category_obj
