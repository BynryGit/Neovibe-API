__author__ = "aki"

from v1.supplier.models.product_category import get_supplier_product_category_by_id_string
from v1.supplier.models.product_subcategory import get_supplier_product_subcategory_by_id_string
from v1.supplier.models.supplier import get_supplier_by_id_string
from v1.supplier.models.supplier_invoice import get_supplier_invoice_by_id_string
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
    # Todo for contract, supplier finacial and demand
    # if "contract" in validated_data:
    #     contract = get_supplier_by_id_string(validated_data["contract"])
    #     validated_data["contract"] = contract.id
    # if "supplier_financial" in validated_data:
    #     supplier_financial = get_supplier_by_id_string(validated_data["supplier_financial"])
    #     validated_data["supplier_financial"] = supplier_financial.id
    # if "demand" in validated_data:
    #     demand = get_supplier_by_id_string(validated_data["demand"])
    #     validated_data["demand"] = demand.id
    return validated_data


def set_supplier_payment_validated_data(validated_data):
    if "invoice" in validated_data:
        invoice = get_supplier_invoice_by_id_string(validated_data["invoice"])
        validated_data["invoice"] = invoice.id
    # Todo for contract, supplier finacial and demand
    # if "contract" in validated_data:
    #     contract = get_supplier_by_id_string(validated_data["contract"])
    #     validated_data["contract"] = contract.id
    # if "supplier_financial" in validated_data:
    #     supplier_financial = get_supplier_by_id_string(validated_data["supplier_financial"])
    #     validated_data["supplier_financial"] = supplier_financial.id
    # if "demand" in validated_data:
    #     demand = get_supplier_by_id_string(validated_data["demand"])
    #     validated_data["demand"] = demand.id
    return validated_data


def set_supplier_product_validated_data(validated_data):
    if "supplier" in validated_data:
        supplier = get_supplier_by_id_string(validated_data["supplier"])
        validated_data["supplier"] = supplier.id
    if "product_category" in validated_data:
        product_category = get_supplier_product_category_by_id_string(validated_data["product_category"])
        validated_data["product_category"] = product_category.id
    if "product_subcategory" in validated_data:
        product_category = get_supplier_product_subcategory_by_id_string(validated_data["product_category"])
        validated_data["product_category"] = product_category.id
    return validated_data


def set_supplier_service_validated_data(validated_data):
    if "supplier" in validated_data:
        supplier = get_supplier_by_id_string(validated_data["supplier"])
        validated_data["supplier"] = supplier.id
    return validated_data


def set_supplier_contract_validated_data(validated_data):
    if "supplier" in validated_data:
        supplier = get_supplier_by_id_string(validated_data["supplier"])
        validated_data["supplier"] = supplier.id
    return validated_data