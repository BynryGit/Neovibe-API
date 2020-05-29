from django.contrib import admin

from v1.contract.models.contract_period import ContractPeriod
from v1.contract.models.contract_status import ContractStatus
from v1.contract.models.contract_type import ContractType
from v1.contract.models.contract import Contract
from v1.contract.models.contract_demand import ContractDemand
from v1.contract.models.terms_and_conditions import TermsAndCondition

admin.site.register(ContractPeriod)
admin.site.register(ContractType)
admin.site.register(Contract)
admin.site.register(ContractDemand)
admin.site.register(TermsAndCondition)
admin.site.register(ContractStatus)
