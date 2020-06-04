__author__ = "aki"

from rest_framework import serializers
from v1.tenant.models.tenant_subscription_plan_rate import TenantSubscriptionPlanRate as TenantSubscriptionPlanRateTbl


class TenantSubscriptionPlanRateViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantSubscriptionPlanRateTbl
        fields = ('id_string', 'subscription_name', 'subscription_type', 'base_rate', 'currency', 'is_taxable', 'tax',
                  'effective_date', 'created_date', 'updated_date')