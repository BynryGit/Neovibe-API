__author__ = "aki"

from v1.contract.models.contract_period import get_contract_period_by_id_string
from v1.contract.models.contract_type import get_contract_type_by_id_string
from v1.supplier.models.supplier_invoice import get_supplier_invoice_by_id_string


def set_contract_validated_data(validated_data):
    if "contract_type" in validated_data:
        contract_type = get_contract_type_by_id_string(validated_data["contract_type"])
        validated_data["contract_type"] = contract_type.id
    if "contract_period" in validated_data:
        contract_period = get_contract_period_by_id_string(validated_data["contract_period"])
        validated_data["contract_period"] = contract_period.id
    # Todo for status and cost center
    # if "status" in validated_data:
    #     status = get_supplier_by_id_string(validated_data["status"])
    #     validated_data["status"] = status.id
    # if "cost_center" in validated_data:
    #     cost_center = get_supplier_by_id_string(validated_data["cost_center"])
    #     validated_data["cost_center"] = cost_center.id
    return validated_data


def set_contract_invoice_validated_data(validated_data):
    # Todo for demand
    # if "demand" in validated_data:
    #     demand = get_supplier_by_id_string(validated_data["demand"])
    #     validated_data["demand"] = demand.id
    return validated_data


def set_contract_payment_validated_data(validated_data):
    if "invoice" in validated_data:
        invoice = get_supplier_invoice_by_id_string(validated_data["invoice"])
        validated_data["invoice"] = invoice.id
    # Todo for contract, supplier finacial and demand
    # if "demand" in validated_data:
    #     demand = get_supplier_by_id_string(validated_data["demand"])
    #     validated_data["demand"] = demand.id
    return validated_data