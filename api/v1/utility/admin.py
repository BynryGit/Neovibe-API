__author__ = "aki"

from django.contrib import admin
from v1.utility.models.mandatory_fields import UtilityMandetoryFields
from v1.utility.models.utility_currency import UtilityCurrency
from v1.utility.models.utility_master import UtilityMaster
from v1.utility.models.utility_module import UtilityModule
from v1.utility.models.utility_service import UtilityService
from v1.utility.models.utility_service_contract_master import UtilityServiceContractMaster
from v1.utility.models.utility_service_contract_template import UtilityServiceContractTemplate
from v1.utility.models.utility_service_master import UtilityServiceMaster
from v1.utility.models.utility_service_plan import UtilityServicePlan
from v1.utility.models.utility_service_plan_rate import UtilityServicePlanRate
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat
from v1.utility.models.utility_status import UtilityStatus
from v1.utility.models.utility_sub_module import UtilitySubModule
from v1.utility.models.utility_usage_summary import UtilityUsageSummary
from v1.utility.models.utility_region import UtilityRegion
from v1.utility.models.utility_payment_channel import UtilityPaymentChannel
from v1.utility.models.utility_payment_type import UtilityPaymentType
from v1.utility.models.utility_payment_subtype import UtilityPaymentSubtype
from v1.utility.models.utility_payment_mode import UtilityPaymentMode
from v1.utility.models.utility_holiday_calendar import UtilityHolidayCalendar
from v1.utility.models.utility_leave_type import UtilityLeaveType

admin.site.register(UtilityModule)
admin.site.register(UtilitySubModule)
admin.site.register(UtilityServicePlan)
admin.site.register(UtilityMandetoryFields)
admin.site.register(UtilityMaster)
admin.site.register(UtilityServicePlanRate)
admin.site.register(UtilityServiceNumberFormat)
admin.site.register(UtilityStatus)
admin.site.register(UtilityUsageSummary)
admin.site.register(UtilityCurrency)
admin.site.register(UtilityRegion)
admin.site.register(UtilityPaymentChannel)
admin.site.register(UtilityPaymentType)
admin.site.register(UtilityPaymentSubtype)
admin.site.register(UtilityPaymentMode)
admin.site.register(UtilityService)
admin.site.register(UtilityServiceContractMaster)
admin.site.register(UtilityServiceContractTemplate)
admin.site.register(UtilityServiceMaster)
admin.site.register(UtilityHolidayCalendar)
admin.site.register(UtilityLeaveType)