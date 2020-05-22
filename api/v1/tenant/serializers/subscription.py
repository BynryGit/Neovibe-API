import uuid
from datetime import datetime
from django.db import transaction
from rest_framework import serializers

from v1.tenant.models.tenant_subscription import TenantSubscription
from v1.tenant.views.common_functions import set_validated_data

class SubscriptionListSerializer(serializers.ModelSerializer):
    # status = TenantStatusViewSerializer(many=False, required=True, source='get_status')

    class Meta:
        model = TenantSubscription
        fields = ('id_string','tenant','subscription_plan_id','subscription_frequency_id',
                   'start_date','end_date','validity_id','is_active')

class SubscriptionViewSerializer(serializers.ModelSerializer):
    #status = TenantStatusViewSerializer(many=False, source='get_status')
    # area = AreaListSerializer(many=False, source='get_area')
    # tenant = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = TenantSubscription
        fields = ('id_string', 'tenant', 'subscription_plan_id', 'subscription_frequency_id',
                  'start_date','end_date', 'validity_id', 'is_active')


class SubscriptionSerializer(serializers.ModelSerializer):

    id_string = serializers.CharField(required=False, max_length=200)
    tenant = serializers.CharField(required=False, max_length=200)
    subscription_plan_id = serializers.CharField(required=False, max_length=200)
    subscription_frequency_id = serializers.CharField(required=False, max_length=200)
    start_date = serializers.CharField(required=False, max_length=200)
    end_date = serializers.CharField(required=False, max_length=200)
    validity_id = serializers.CharField(required=False, max_length=200)
    is_active = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = TenantSubscription
        fields = ('__all__')

    def create(self, validated_data):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            subscription_obj = super(SubscriptionSerializer, self).create(validated_data)
            # tenant_obj.created_by = user.id
            # tenant_obj.created_date = datetime.utcnow()
            # tenant_obj.tenant = user.tenant
            subscription_obj.save()
            return subscription_obj

    def update(self, instance, validated_data):
        validated_data = set_validated_data(validated_data)
        with transaction.atomic():
            subscription_obj = super(SubscriptionSerializer, self).update(instance, validated_data)
            # tenant_obj.updated_by = user.id
            # tenant_obj.updated_date = datetime.utcnow()
            subscription_obj.save()
            return subscription_obj