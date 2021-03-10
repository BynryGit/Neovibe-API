from datetime import datetime

from pkg_resources import require
from v1.consumer.models.consumer_service_contract_details import get_consumer_service_contract_detail_by_id_string
from django.db import transaction
from rest_framework import serializers, status
from api.messages import CONSUMER_OFFER_ALREADY_EXISTS
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.consumer.models.consumer_offer_detail import ConsumerOfferDetail
from v1.consumer.views.common_functions import set_consumer_offer_detail_validated_data


class ConsumerOfferDetailListSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ConsumerOfferDetail
        fields = ('tenant', 'tenant_id_string', 'utility', 'utility_id_string',)


class ConsumerOfferDetailSerializer(serializers.ModelSerializer):
    offer_id = serializers.CharField(required=False, max_length=200)
    utility = serializers.CharField(required=False, max_length=200)
    consumer_service_contract_detail_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ConsumerOfferDetail
        fields = '__all__'

    def create(self, validated_data, consumer_obj, user):
        validated_data = set_consumer_offer_detail_validated_data(validated_data)

        if ConsumerOfferDetail.objects.filter(consumer_id=consumer_obj.id,
                                              offer_id=validated_data['offer_id'],
                                              is_active=True).exists():
            raise CustomAPIException(CONSUMER_OFFER_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                consumer_offer_detail = super(ConsumerOfferDetailSerializer, self).create(validated_data=validated_data)
                consumer_offer_detail.tenant = consumer_obj.tenant
                consumer_offer_detail.utility = consumer_obj.utility
                consumer_offer_detail.consumer_id = consumer_obj.id
                consumer_offer_detail.created_by = user.id
                consumer_offer_detail.created_date = datetime.now()
                consumer_offer_detail.is_active = True
                consumer_offer_detail.save()
                return consumer_offer_detail
