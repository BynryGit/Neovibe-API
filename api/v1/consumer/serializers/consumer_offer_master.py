from rest_framework import serializers,status
from v1.consumer.models.consumer_offer_master import ConsumerOfferMaster as ConsumerOfferMasterTbl
from v1.consumer.serializers.offer_sub_type import OfferSubTypeListSerializer
from api.messages import CONSUMER_OFFER_ALREADY_EXISTS
from v1.utility.serializers.utility_sub_module import UtilitySubModuleListSerializer
from datetime import datetime
from django.db import transaction
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.consumer.views.common_functions import set_consumer_offer_master_validated_data


class ConsumerOfferMasterListSerializer(serializers.ModelSerializer):
    offer_sub_type = OfferSubTypeListSerializer(source='get_offer_sub_type')
    sub_module = UtilitySubModuleListSerializer(source='get_sub_module')

    class Meta:
        model = ConsumerOfferMasterTbl
        fields = ('offer_name', 'id_string', 'service_obj' , 'sub_module', 'offer_code', 'offer_sub_type')


class ConsumerOfferMasterViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ConsumerOfferMasterTbl
        fields = (
            'tenant', 'tenant_id_string', 'utility', 'offer_percentage', 'utility_id_string', 'offer_name', 'id_string')


class ConsumerOfferMasterSerializer(serializers.ModelSerializer):
    offer_name = serializers.CharField(required=True, max_length=200,
                                       error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    offer_type_id = serializers.CharField(required=False, max_length=200)
    offer_sub_type_id = serializers.CharField(required=False, max_length=200)
    module_id = serializers.CharField(required=False, max_length=200)
    submodule_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ConsumerOfferMasterTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_consumer_offer_master_validated_data(validated_data)
            if ConsumerOfferMasterTbl.objects.filter(offer_name=validated_data['offer_name'], tenant_id=validated_data['tenant_id'],
                                                     utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(CONSUMER_OFFER_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
            else:
                consumer_offer_obj = super(ConsumerOfferMasterSerializer, self).create(validated_data)
                consumer_offer_obj.created_by = user.id
                consumer_offer_obj.updated_by = user.id
                consumer_offer_obj.save()
                return consumer_offer_obj

    def update(self, instance, validated_data, user):
        validated_data = set_consumer_offer_master_validated_data(validated_data)
        with transaction.atomic():
            consumer_offer_obj = super(ConsumerOfferMasterSerializer, self).update(instance, validated_data)
            consumer_offer_obj.updated_by = user.id
            consumer_offer_obj.updated_date = datetime.utcnow()
            consumer_offer_obj.save()
            return consumer_offer_obj
