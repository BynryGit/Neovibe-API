import uuid
from datetime import datetime
from django.db import transaction
from rest_framework import serializers

from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.country import get_country_by_id_string
from v1.commonapp.models.state import get_state_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.commonapp.serializers.area import AreaListSerializer
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string
from v1.consumer.models.consumer_ownership import get_consumer_ownership_by_id_string
from v1.consumer.models.consumer_scheme_master import get_scheme_by_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.consumer.models.source_type import get_source_type_by_id_string
from v1.payment.models.consumer_payment import get_payment_by_id_string
from v1.registration.models.registration_status import RegistrationStatus, get_registration_status_by_id_string
from v1.registration.models.registration_type import get_registration_type_by_id_string
from v1.registration.models.registrations import Registration
from v1.registration.views.common_functions import set_validated_data
from v1.tenant.models.tenant_master import TenantMaster
from v1.tenant.models.tenant_status import TenantStatus


class TenantStatusViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantStatus
        fields = ('name','id_string')


class TenantListSerializer(serializers.ModelSerializer):
    status = TenantStatusViewSerializer(many=False, required=True, source='get_status')

    class Meta:
        model = TenantMaster
        fields = ('id_string','short_name','name','email_id','mobile_no','region_id','country_id','state_id','status_id','is_active','created_by','created_date')

class TenantViewSerializer(serializers.ModelSerializer):
    status = TenantStatusViewSerializer(many=False, source='get_status')
    area = AreaListSerializer(many=False, source='get_area')
    tenant = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = TenantMaster
        fields = (
        'id_string', 'short_name', 'name', 'email_id', 'mobile_no', 'region_id', 'country_id', 'state_id', 'status_id',
        'is_active', 'created_by', 'created_date')


class TenantSerializer(serializers.ModelSerializer):
    id_string = serializers.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    short_name = serializers.BigIntegerField(null=True, blank=True)
    name = serializers.CharField(max_length=200, blank=False, null=False)
    email_id = serializers.CharField(max_length=200, null=True, blank=True)
    mobile_no = serializers.CharField(max_length=200, blank=True, null=True)
    region_id = serializers.BigIntegerField(null=True, blank=True)
    country_id = serializers.BigIntegerField(null=True, blank=True)
    state_id = serializers.BigIntegerField(null=True, blank=True)
    status_id = serializers.BigIntegerField(null=True, blank=True)
    is_active = serializers.BooleanField(default=False)

    class Meta:
        model = TenantMaster
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data =  set_validated_data(validated_data)
        with transaction.atomic():
            payments = []
            if 'payments' in validated_data:
                payments = validated_data.pop('payments')

            registration_obj = super(TenantSerializer, self).create(validated_data)
            registration_obj.created_by = user.id
            registration_obj.created_date = datetime.now()
            registration_obj.tenant = user.tenant
            registration_obj.utility = user.utility
            registration_obj.save()
            if payments:
                for payment in payments:
                    payment['identification'] = registration_obj.id
                    payment_obj = PaymentSerializer(**payment)
            return registration_obj

    def update(self, instance, validated_data, user):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            payments = []
            if 'payments' in validated_data:
                payments = validated_data.pop('payments')

            registration_obj = super(TenantSerializer, self).update(instance, validated_data)
            registration_obj.updated_by = user
            registration_obj.updated_date = datetime.now()
            registration_obj.save()
            if payments:
                for payment in payments:
                    payment['identification'] = registration_obj.id
                    payment_obj = PaymentSerializer(**payment)
            return registration_obj