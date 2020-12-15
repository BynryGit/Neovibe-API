__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers, status

from api.messages import SUBSCRIPTION_ALREADY_EXIST
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.models.tenant_subscription import TenantSubscription as TenantSubscriptionTbl
from v1.tenant.serializers.tenant_subscription_plan import TenantSubscriptionPlanViewSerializer
from v1.tenant.serializers.tenant_subscription_plan_rate import TenantSubscriptionPlanRateViewSerializer
from v1.tenant.views.common_functions import set_tenant_subscription_validated_data


class TenantSubscriptionShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantSubscriptionTbl
        fields = ('id_string', 'start_date','end_date', 'validity_id', 'created_date', 'updated_date')


class TenantSubscriptionViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(read_only=True)
    subscription_plan_id = TenantSubscriptionPlanViewSerializer(many=False, required=False, source='get_subscription_plan_id')
    subscription_rate_id = TenantSubscriptionPlanRateViewSerializer(many=False, required=False, source='get_subscription_rate_id')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = TenantSubscriptionTbl
        fields = ('id_string', 'start_date','end_date', 'validity_id', 'created_date', 'updated_date',
                  'subscription_plan_id', 'subscription_rate_id', 'tenant')


class TenantSubscriptionSerializer(serializers.ModelSerializer):
    subscription_plan_id = serializers.UUIDField(required=True)
    subscription_rate_id = serializers.UUIDField(required=True)

    class Meta:
        model = TenantSubscriptionTbl
        fields = ('__all__')

    def create(self, validated_data, tenant_obj, user):
        validated_data = set_tenant_subscription_validated_data(validated_data)
        if TenantSubscriptionTbl.objects.filter(tenant=tenant_obj,
                                                subscription_plan_id=validated_data["subscription_plan_id"],
                                                subscription_rate_id=validated_data["subscription_rate_id"]).exists():
            raise CustomAPIException(SUBSCRIPTION_ALREADY_EXIST,status_code=status.HTTP_409_CONFLICT)
        with transaction.atomic():
            tenant_subscription_obj = super(TenantSubscriptionSerializer, self).create(validated_data)
            tenant_subscription_obj.tenant = tenant_obj
            tenant_subscription_obj.created_by = user.id
            tenant_subscription_obj.save()
            return tenant_subscription_obj

    def update(self, instance, validated_data, user):
        validated_data = set_tenant_subscription_validated_data(validated_data)
        with transaction.atomic():
            tenant_subscription_obj = super(TenantSubscriptionSerializer, self).update(instance, validated_data)
            tenant_subscription_obj.updated_date = timezone.now()
            tenant_subscription_obj.save()
            return tenant_subscription_obj
