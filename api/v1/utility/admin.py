__author__ = "aki"

from django.contrib import admin
from v1.utility.models.mandatory_fields import UtilityMandetoryFields
from v1.utility.models.utility_master import UtilityMaster
from v1.utility.models.utility_module import UtilityModule
from v1.utility.models.utility_service_plan import UtilityServicePlan
from v1.utility.models.utility_service_plan_rate import UtilityServicePlanRate
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat
from v1.utility.models.utility_status import UtilityStatus
from v1.utility.models.utility_sub_module import UtilitySubModule
from v1.utility.models.utility_usage_summary import UtilityUsageSummary

admin.site.register(UtilityModule)
admin.site.register(UtilitySubModule)
admin.site.register(UtilityServicePlan)
admin.site.register(UtilityMandetoryFields)
admin.site.register(UtilityMaster)
admin.site.register(UtilityServicePlanRate)
admin.site.register(UtilityServiceNumberFormat)
admin.site.register(UtilityStatus)
admin.site.register(UtilityUsageSummary)
