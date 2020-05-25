from django.contrib import admin
from v1.tenant.models.tenant_master import TenantMaster
from v1.tenant.models.tenant_subscription_plan import TenantSubscriptionPlan
from v1.tenant.models.tenant_subscription_plan_rate import TenantSubscriptionPlanRate
from v1.tenant.models.tenant_bank_details import TenantBankDetails
from v1.tenant.models.tenant_city import TenantCity
from v1.tenant.models.tenant_country import TenantCountry
from v1.tenant.models.tenant_currency import TenantCurrency
from v1.tenant.models.tenant_invoice_details import TenantInvoiceDetails
from v1.tenant.models.tenant_invoice_payment import TenantInvoicePayment
from v1.tenant.models.tenant_invoices import TenantInvoices
from v1.tenant.models.tenant_sub_module import TenantSubModule
from v1.tenant.models.tenant_module import TenantModule
from v1.tenant.models.tenant_subscription import TenantSubscription
from v1.tenant.models.tenant_summary_on_monthly_basis import TenantSummaryOnMonthlyBasis



admin.site.register(TenantMaster)
admin.site.register(TenantSubscriptionPlan)
admin.site.register(TenantSubscriptionPlanRate)
admin.site.register(TenantBankDetails)
admin.site.register(TenantCity)
admin.site.register(TenantCountry)
admin.site.register(TenantInvoiceDetails)
admin.site.register(TenantInvoicePayment)
admin.site.register(TenantInvoices)
admin.site.register(TenantModule)
admin.site.register(TenantSubModule)
admin.site.register(TenantSubscription)
admin.site.register(TenantSummaryOnMonthlyBasis)


