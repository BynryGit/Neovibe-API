import uuid
from datetime import datetime
from django.db import transaction
from rest_framework import serializers

from v1.tenant.models.tenant_subscription_plan_rate import TenantSubscriptionPlanRate
from v1.tenant.views.common_functions import set_validated_data

class SubscriptionPlanRateListSerializer(serializers.ModelSerializer):
    # status = TenantStatusViewSerializer(many=False, required=True, source='get_status')

    class Meta:
        model = TenantSubscriptionPlanRate
        fields = ('id_string', 'tenantsubscriptionplan_id', 'base_rate', 'currency', 'region',
                  'country', 'is_taxable', 'tax', 'effective_date', 'is_active')

class SubscriptionPlanViewSerializer(serializers.ModelSerializer):
    #status = TenantStatusViewSerializer(many=False, source='get_status')
    # area = AreaListSerializer(many=False, source='get_area')
    # tenant = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = TenantSubscriptionPlanRate
        fields = ('id_string', 'tenantsubscriptionplan_id','base_rate','currency','region',
                  'country','is_taxable', 'tax','effective_date', 'is_active')


class SubscriptionPlanRateSerializer(serializers.ModelSerializer):

    id_string = serializers.CharField(required=False, max_length=200)
    subscription_plan_id = serializers.CharField(required=False, max_length=200)
    base_rate = serializers.CharField(required=False, max_length=200)
    currency = serializers.CharField(required=False, max_length=200)
    region = serializers.CharField(required=False, max_length=200)
    country = serializers.CharField(required=False, max_length=200)
    is_taxable = serializers.CharField(required=False, max_length=200)
    tax = serializers.CharField(required=False, max_length=200)
    effective_date = serializers.CharField(required=False, max_length=200)
    is_active = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = TenantSubscriptionPlanRate
        fields = ('__all__')

    def create(self, validated_data):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            subscription_plan__rate_obj = super(SubscriptionPlanRateSerializer, self).create(validated_data)
            # tenant_obj.created_by = user.id
            # tenant_obj.created_date = datetime.utcnow()
            # tenant_obj.tenant = user.tenant
            subscription_plan__rate_obj.save()
            return subscription_plan__rate_obj

    def update(self, instance, validated_data):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            subscription_plan_rate_obj = super(SubscriptionPlanRateSerializer, self).update(instance, validated_data)
            # tenant_obj.updated_by = user.id
            # tenant_obj.updated_date = datetime.utcnow()
            subscription_plan_rate_obj.save()
            return subscription_plan_rate_obj