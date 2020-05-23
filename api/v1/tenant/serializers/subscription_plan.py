import uuid
from datetime import datetime
from django.db import transaction
from rest_framework import serializers

from v1.tenant.models.tenant_subscription_plan import TenantSubscriptionPlan
from v1.tenant.views.common_functions import set_validated_data, set_validated_data_subscription_plan


class SubscriptionPlanListSerializer(serializers.ModelSerializer):
    # status = TenantStatusViewSerializer(many=False, required=True, source='get_status')

    class Meta:
        model = TenantSubscriptionPlan
        fields = ( 'id_string','subscription_id','short_name','subcription_type','subscription_name',
                   'description','max_utility','max_user','max_consumer','max_storage','is_active')

class SubscriptionPlanViewSerializer(serializers.ModelSerializer):
    #status = TenantStatusViewSerializer(many=False, source='get_status')
    # area = AreaListSerializer(many=False, source='get_area')
    # tenant = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = TenantSubscriptionPlan
        fields = ('id_string', 'subscription_id', 'short_name', 'subcription_type','subscription_name',
                  'description', 'max_utility', 'max_user', 'max_consumer', 'max_storage', 'is_active')


class SubscriptionPlanSerializer(serializers.ModelSerializer):

    id_string = serializers.CharField(required=False, max_length=200)
    subscription_id = serializers.CharField(required=False, max_length=200)
    subscription_name = serializers.CharField(required=False, max_length=200)
    short_name = serializers.CharField(required=False, max_length=200)
    subcription_type = serializers.CharField(required=False, max_length=200)
    description = serializers.CharField(required=False, max_length=200)
    max_utility = serializers.CharField(required=False, max_length=200)
    max_user = serializers.CharField(required=False, max_length=200)
    max_consumer = serializers.CharField(required=False, max_length=200)
    max_storage = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = TenantSubscriptionPlan
        fields = ('__all__')

    def create(self, validated_data):
        validated_data = set_validated_data_subscription_plan(validated_data)
        with transaction.atomic():
            subscription_plan_obj = super(SubscriptionPlanSerializer, self).create(validated_data)
            # tenant_obj.created_by = user.id
            # tenant_obj.created_date = datetime.utcnow()
            # tenant_obj.tenant = user.tenant
            subscription_plan_obj.save()
            return subscription_plan_obj

    def update(self, instance, validated_data):
        validated_data = set_validated_data_subscription_plan(validated_data)
        with transaction.atomic():
            subscription_plan_obj = super(SubscriptionPlanSerializer, self).update(instance, validated_data)
            # tenant_obj.updated_by = user.id
            # tenant_obj.updated_date = datetime.utcnow()
            subscription_plan_obj.save()
            return subscription_plan_obj