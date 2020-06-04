__author__ = "aki"

from rest_framework import serializers
from v1.tenant.models.tenant_subscription_plan import TenantSubscriptionPlan as TenantSubscriptionPlanTbl


class TenantSubscriptionPlanViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantSubscriptionPlanTbl
        fields = ('id_string', 'subscription_type', 'subscription_name', 'short_name','description',
                  'max_utility', 'max_user', 'max_consumer', 'max_storage', 'created_date', 'updated_date')