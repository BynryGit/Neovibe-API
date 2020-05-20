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
from v1.tenant.models.tenant_master import TenantMaster
from v1.tenant.models.tenant_status import TenantStatus
from v1.tenant.views.common_functions import set_validated_data


class TenantStatusViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantStatus
        fields = ('name','id_string')


class TenantListSerializer(serializers.ModelSerializer):
    # status = TenantStatusViewSerializer(many=False, required=True, source='get_status')

    class Meta:
        model = TenantMaster
        fields = ( 'id_string','subscription_id','module_id','sub_module_id','sub_module_name','is_active')

class TenantViewSerializer(serializers.ModelSerializer):
    #status = TenantStatusViewSerializer(many=False, source='get_status')
    # area = AreaListSerializer(many=False, source='get_area')
    # tenant = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = TenantMaster
        fields = (
        'id_string', 'short_name', 'name', 'email_id', 'mobile_no', 'city_id', 'country_id', 'state_id', 'status_id')


class TenantSerializer(serializers.ModelSerializer):

    id_string = serializers.CharField(required=False, max_length=200)
    short_name = serializers.CharField(required=False, max_length=200)
    name = serializers.CharField(required=False, max_length=200)
    email_id = serializers.CharField(required=False, max_length=200)
    mobile_no = serializers.CharField(required=False, max_length=200)
    city_id = serializers.CharField(required=False, max_length=200)
    country_id = serializers.CharField(required=False, max_length=200)
    state_id = serializers.CharField(required=False, max_length=200)
    status_id = serializers.CharField(required=False, max_length=200)
    is_active = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = TenantMaster
        fields = ('__all__')

    def create(self, validated_data):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            tenant_obj = super(TenantSerializer, self).create(validated_data)
            # tenant_obj.created_by = user.id
            # tenant_obj.created_date = datetime.utcnow()
            # tenant_obj.tenant = user.tenant
            tenant_obj.save()
            return tenant_obj

    def update(self, instance, validated_data):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            tenant_obj = super(TenantSerializer, self).update(instance, validated_data)
            # tenant_obj.updated_by = user.id
            # tenant_obj.updated_date = datetime.utcnow()
            tenant_obj.save()
            return tenant_obj