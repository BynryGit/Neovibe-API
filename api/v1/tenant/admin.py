from django.contrib import admin
from v1.tenant.models.tenant_master import TenantMaster
from v1.tenant.models.tenant_subscription_plan import TenantSubscriptionPlan
from v1.tenant.models.tenant_subscription_plan_rate import TenantSubscriptionPlanRate
from v1.utility.models.utility_master import UtilityMaster

admin.site.register(TenantMaster)
admin.site.register(TenantSubscriptionPlan)
admin.site.register(TenantSubscriptionPlanRate)