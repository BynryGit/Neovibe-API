__author__ = "aki"

from v1.commonapp.models.module import get_module_by_id_string
from v1.commonapp.models.sub_module import get_sub_module_by_id_string
from v1.tenant.models.tenant_bank_details import get_tenant_bank_details_by_id_string
from v1.tenant.models.tenant_city import get_tenant_city_by_id_string
from v1.tenant.models.tenant_country import get_tenant_country_by_id_string
from v1.tenant.models.tenant_invoice import get_tenant_invoice_by_id_string
from v1.tenant.models.tenant_state import get_tenant_state_by_id_string
from v1.tenant.models.tenant_status import get_tenant_status_by_id_string
from v1.tenant.models.tenant_subscription import get_tenant_subscription_by_id_string
from v1.tenant.models.tenant_subscription_plan import get_tenant_subscription_plan_by_id_string
from v1.tenant.models.tenant_subscription_plan_rate import get_tenant_subscription_plan_rate_by_id_string


def set_tenant_validated_data(validated_data):
    if "tenant_country_id" in validated_data:
        tenant_country = get_tenant_country_by_id_string(validated_data["tenant_country_id"])
        validated_data["tenant_country_id"] = tenant_country.id
    if "tenant_state_id" in validated_data:
        tenant_state = get_tenant_state_by_id_string(validated_data["tenant_state_id"])
        validated_data["tenant_state_id"] = tenant_state.id
    if "tenant_city_id" in validated_data:
        tenant_city = get_tenant_city_by_id_string(validated_data["tenant_city_id"])
        validated_data["tenant_city_id"] = tenant_city.id
    if "status_id" in validated_data:
        tenant_status = get_tenant_status_by_id_string(validated_data["status_id"])
        validated_data["status_id"] = tenant_status.id
    return validated_data


def set_tenant_module_validated_data(validated_data):
    if "module_id" in validated_data:
        module = get_module_by_id_string(validated_data["module_id"])
        validated_data["module_id"] = module.id
    return validated_data


def set_tenant_sub_module_validated_data(validated_data):
    if "sub_module_id" in validated_data:
        sub_module = get_sub_module_by_id_string(validated_data["sub_module_id"])
        validated_data["module_id"] = sub_module.module_id
        validated_data["sub_module_id"] = sub_module.id
    return validated_data


def set_tenant_subscription_validated_data(validated_data):
    if "subscription_plan_id" in validated_data:
        subscription_plan = get_tenant_subscription_plan_by_id_string(validated_data["subscription_plan_id"])
        validated_data["subscription_plan_id"] = subscription_plan.id
    if "subscription_rate_id" in validated_data:
        subscription_rate = get_tenant_subscription_plan_rate_by_id_string(validated_data["subscription_rate_id"])
        validated_data["subscription_rate_id"] = subscription_rate.id
    return validated_data


def set_tenant_invoice_validated_data(validated_data):
    if "tenant_subscription_id" in validated_data:
        tenant_subscription = get_tenant_subscription_by_id_string(validated_data["tenant_subscription_id"])
        validated_data["tenant_subscription_id"] = tenant_subscription.id
    if "tenant_bank_detail_id" in validated_data:
        tenant_bank_detail = get_tenant_bank_details_by_id_string(validated_data["tenant_bank_detail_id"])
        validated_data["tenant_bank_detail_id"] = tenant_bank_detail.id
    return validated_data


def set_tenant_invoice_payment_validated_data(validated_data):
    if "invoice_id" in validated_data:
        tenant_invoice = get_tenant_invoice_by_id_string(validated_data["invoice_id"])
        validated_data["invoice_id"] = tenant_invoice.id
    return validated_data