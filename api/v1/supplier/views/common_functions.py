__author__ = "aki"

from v1.contract.models.contract import get_contract_by_id_string
from v1.contract.models.contract_demand import get_contract_demand_by_id_string
from v1.contract.models.contract_period import get_contract_period_by_id_string
from v1.contract.models.contract_status import get_contract_status_by_id_string
from v1.contract.models.contract_type import get_contract_type_by_id_string
from v1.supplier.models.product_category import get_supplier_product_category_by_id_string
from v1.supplier.models.product_subcategory import get_supplier_product_subcategory_by_id_string
from v1.supplier.models.sup_ser_category import get_supplier_service_category_by_id_string
from v1.supplier.models.sup_ser_subcategory import get_supplier_service_subcategory_by_id_string
from v1.supplier.models.supplier_invoice import get_supplier_invoice_by_id_string
from v1.supplier.models.supplier_product import get_supplier_product_by_id_string
from v1.supplier.models.supplier_status import get_supplier_status_by_id_string
from v1.tenant.models.tenant_city import get_tenant_city_by_id_string
from v1.tenant.models.tenant_country import get_tenant_country_by_id_string
from v1.tenant.models.tenant_state import get_tenant_state_by_id_string


def set_supplier_validated_data(validated_data):
    if "country_id" in validated_data:
        country = get_tenant_country_by_id_string(validated_data["country_id"])
        validated_data["country_id"] = country.id
    if "state_id" in validated_data:
        state = get_tenant_state_by_id_string(validated_data["state_id"])
        validated_data["state_id"] = state.id
    if "city_id" in validated_data:
        city = get_tenant_city_by_id_string(validated_data["city_id"])
        validated_data["city_id"] = city.id
    if "status_id" in validated_data:
        status = get_supplier_status_by_id_string(validated_data["status_id"])
        validated_data["status_id"] = status.id
    return validated_data


def set_supplier_invoice_validated_data(validated_data):
    if "contract" in validated_data:
        contract = get_contract_by_id_string(validated_data["contract"])
        validated_data["contract"] = contract.id
    if "demand" in validated_data:
        demand = get_contract_demand_by_id_string(validated_data["demand"])
        validated_data["demand"] = demand.id
    # Todo for supplier finacial
    # if "supplier_financial" in validated_data:
    #     supplier_financial = get_supplier_by_id_string(validated_data["supplier_financial"])
    #     validated_data["supplier_financial"] = supplier_financial.id
    return validated_data


def set_supplier_payment_validated_data(validated_data):
    if "invoice" in validated_data:
        invoice = get_supplier_invoice_by_id_string(validated_data["invoice"])
        validated_data["invoice"] = invoice.id
    if "contract" in validated_data:
        contract = get_contract_by_id_string(validated_data["contract"])
        validated_data["contract"] = contract.id
    if "demand" in validated_data:
        demand = get_contract_demand_by_id_string(validated_data["demand"])
        validated_data["demand"] = demand.id
    # Todo for supplier finacial
    # if "supplier_financial" in validated_data:
    #     supplier_financial = get_supplier_by_id_string(validated_data["supplier_financial"])
    #     validated_data["supplier_financial"] = supplier_financial.id
    return validated_data


def set_supplier_product_validated_data(validated_data):
    if "product_category" in validated_data:
        product_category = get_supplier_product_category_by_id_string(validated_data["product_category"])
        validated_data["product_category"] = product_category.id
    if "product_subcategory" in validated_data:
        product_subcategory = get_supplier_product_subcategory_by_id_string(validated_data["product_subcategory"])
        validated_data["product_subcategory"] = product_subcategory.id
    # Todo for tupe,status and source type
    # if "type" in validated_data:
    #     type = get_supplier_product_subcategory_by_id_string(validated_data["type"])
    #     validated_data["type"] = type.id
    # if "status" in validated_data:
    #     status = get_supplier_product_subcategory_by_id_string(validated_data["status"])
    #     validated_data["status"] = status.id
    # if "source_type" in validated_data:
    #     source_type = get_supplier_product_subcategory_by_id_string(validated_data["source_type"])
    #     validated_data["source_type"] = source_type.id
    return validated_data


def set_supplier_service_validated_data(validated_data):
    if "service_category" in validated_data:
        service_category = get_supplier_service_category_by_id_string(validated_data["service_category"])
        validated_data["service_category"] = service_category.id
    if "service_subcategory" in validated_data:
        service_subcategory = get_supplier_service_subcategory_by_id_string(validated_data["service_subcategory"])
        validated_data["service_subcategory"] = service_subcategory.id
    # Todo for tupe,status and source type
    # if "type" in validated_data:
    #     type = get_supplier_product_subcategory_by_id_string(validated_data["type"])
    #     validated_data["type"] = type.id
    # if "status" in validated_data:
    #     status = get_supplier_product_subcategory_by_id_string(validated_data["status"])
    #     validated_data["status"] = status.id
    # if "source_type" in validated_data:
    #     source_type = get_supplier_product_subcategory_by_id_string(validated_data["source_type"])
    #     validated_data["source_type"] = source_type.id
    return validated_data


def set_supplier_contract_validated_data(validated_data):
    if "contract_type" in validated_data:
        contract_type = get_contract_type_by_id_string(validated_data["contract_type"])
        validated_data["contract_type"] = contract_type.id
    if "contract_period" in validated_data:
        contract_period = get_contract_period_by_id_string(validated_data["contract_period"])
        validated_data["contract_period"] = contract_period.id
    if "supplier_product_id" in validated_data:
        supplier_product_id = get_supplier_product_by_id_string(validated_data["supplier_product_id"])
        validated_data["supplier_product_id"] = supplier_product_id.id
    if "status" in validated_data:
        status = get_contract_status_by_id_string(validated_data["status"])
        validated_data["status"] = status.id
    # Todo for status
    # if "cost_center" in validated_data:
    #     cost_center = get_supplier_by_id_string(validated_data["cost_center"])
    #     validated_data["cost_center"] = cost_center.id
    return validated_data