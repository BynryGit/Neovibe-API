from django.contrib import admin

from v1.contract.models.contract_period import ContractPeriod
from v1.contract.models.contract_type import ContractType
from v1.contract.models.contracts import Contract
from v1.contract.models.contracts_demand import ContractsDemand
from v1.contract.models.terms_and_conditions import TermsAndCondition

admin.site.register(ContractPeriod)
admin.site.register(ContractType)
admin.site.register(Contract)
admin.site.register(ContractsDemand)
admin.site.register(TermsAndCondition)
