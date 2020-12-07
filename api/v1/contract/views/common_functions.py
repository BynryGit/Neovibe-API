__author__ = "aki"

from rest_framework import status
from v1.contract.models.contract_demand import get_contract_demand_by_id_string
from v1.contract.models.contract_period import get_contract_period_by_id_string
from v1.contract.models.contract_status import get_contract_status_by_id_string
from v1.contract.models.contract_type import get_contract_type_by_id_string
from v1.supplier.models.supplier_invoice import get_supplier_invoice_by_id_string
from v1.supplier.models.supplier_product import get_supplier_product_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.contract.models.contract_subtype import get_contract_subtype_by_id_string
from v1.contract.models.terms_and_conditions import get_contract_term_and_condition_by_id_string
from v1.contract.models.contract import get_contract_by_id_string
from api.messages import NAME_ALREADY_EXIST, CONTRACT_TYPE_NOT_FOUND, CONTRACT_SUBTYPE_NOT_FOUND, CONTRACT_PERIOD_NOT_FOUND, TERMS_AND_CONDITION_NOT_FOUND, UTILITY_NOT_FOUND, TENANT_NOT_FOUND, CONTRACT_NOT_FOUND


def set_contract_validated_data(validated_data):
    if "contract_type" in validated_data:
        contract_type = get_contract_type_by_id_string(validated_data["contract_type"])
        if contract_type:
            validated_data["contract_type"] = contract_type.id
        else:
            raise CustomAPIException(CONTRACT_TYPE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "contract_subtype" in validated_data:
        contract_subtype = get_contract_subtype_by_id_string(validated_data["contract_subtype"])
        if contract_subtype:
            validated_data["contract_subtype"] = contract_subtype.id
        else:
            raise CustomAPIException(CONTRACT_SUBTYPE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "contract_period" in validated_data:
        contract_period = get_contract_period_by_id_string(validated_data["contract_period"])
        if contract_period:
            validated_data["contract_period"] = contract_period.id
        else:
            raise CustomAPIException(CONTRACT_PERIOD_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "contract_termsandcondition" in validated_data:
        contract_termsandcondition = get_contract_term_and_condition_by_id_string(validated_data["contract_termsandcondition"])
        if contract_termsandcondition:
            validated_data["contract_termsandcondition"] = contract_termsandcondition.id
        else:
            raise CustomAPIException(TERMS_AND_CONDITION_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    # if "status" in validated_data:
    #     status = get_contract_status_by_id_string(validated_data["status"])
    #     if status:
    #         validated_data["status"] = status.id
    #     else:
    #         raise CustomAPIException("Status not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException(UTILITY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException(TENANT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "type_id" in validated_data:
        contract_type = get_contract_type_by_id_string(validated_data["type_id"])
        if contract_type:
            validated_data["type_id"] = contract_type.id
        else:
            raise CustomAPIException(CONTRACT_TYPE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "contract" in validated_data:
        contract = get_contract_by_id_string(validated_data["contract"])
        if contract:
            validated_data["contract"] = contract.id
        else:
            raise CustomAPIException(CONTRACT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    # Todo for cost_center
    # if "cost_center" in validated_data:
    #     cost_center = get_supplier_by_id_string(validated_data["cost_center"])
    #     validated_data["cost_center"] = cost_center.id
    return validated_data


def set_contract_invoice_validated_data(validated_data):
    if "demand" in validated_data:
        demand = get_contract_demand_by_id_string(validated_data["demand"])
        validated_data["demand"] = demand.id
    return validated_data


def set_contract_payment_validated_data(validated_data):
    if "invoice" in validated_data:
        invoice = get_supplier_invoice_by_id_string(validated_data["invoice"])
        validated_data["invoice"] = invoice.id
    if "demand" in validated_data:
        demand = get_contract_demand_by_id_string(validated_data["demand"])
        validated_data["demand"] = demand.id
    return validated_data


def set_contract_demand_validated_data(validated_data):
    if "supplier_product" in validated_data:
        supplier_product = get_supplier_product_by_id_string(validated_data["supplier_product"])
        validated_data["supplier_product"] = supplier_product.id
    # Todo for status
    # if "status" in validated_data:
    #     status = get_supplier_by_id_string(validated_data["status"])
    #     validated_data["status"] = status.id
    return validated_data