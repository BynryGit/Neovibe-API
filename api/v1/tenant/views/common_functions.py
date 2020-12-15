__author__ = "aki"

from api.messages import *
from rest_framework import status
from v1.commonapp.models.module import get_module_by_id_string
from v1.commonapp.models.sub_module import get_sub_module_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
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
        if tenant_country:
            validated_data["tenant_country_id"] = tenant_country.id
        else:
            raise CustomAPIException(COUNTRY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_state_id" in validated_data:
        tenant_state = get_tenant_state_by_id_string(validated_data["tenant_state_id"])
        if tenant_state:
            validated_data["tenant_state_id"] = tenant_state.id
        else:
            raise CustomAPIException(STATE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_city_id" in validated_data:
        tenant_city = get_tenant_city_by_id_string(validated_data["tenant_city_id"])
        if tenant_city:
            validated_data["tenant_city_id"] = tenant_city.id
        else:
            raise CustomAPIException(CITY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "status_id" in validated_data:
        tenant_status = get_tenant_status_by_id_string(validated_data["status_id"])
        if tenant_status:
            validated_data["status_id"] = tenant_status.id
        else:
            raise CustomAPIException(STATUS_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_tenant_module_validated_data(validated_data):
    if "module_id" in validated_data:
        module = get_module_by_id_string(validated_data["module_id"])
        if module:
            validated_data["module_id"] = module.id
        else:
            raise CustomAPIException(MODULE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_tenant_sub_module_validated_data(validated_data):
    if "sub_module_id" in validated_data:
        sub_module = get_sub_module_by_id_string(validated_data["sub_module_id"])
        if sub_module:
            validated_data["module_id"] = sub_module.module_id
            validated_data["sub_module_id"] = sub_module.id
        else:
            raise CustomAPIException(SUBMODULE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_tenant_subscription_validated_data(validated_data):
    if "subscription_plan_id" in validated_data:
        subscription_plan = get_tenant_subscription_plan_by_id_string(validated_data["subscription_plan_id"])
        if subscription_plan:
            validated_data["subscription_plan_id"] = subscription_plan.id
        else:
            raise CustomAPIException(SUBSCRIPTION_PLAN_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "subscription_rate_id" in validated_data:
        subscription_rate = get_tenant_subscription_plan_rate_by_id_string(validated_data["subscription_rate_id"])
        if subscription_rate:
            validated_data["subscription_rate_id"] = subscription_rate.id
        else:
            raise CustomAPIException(SUBSCRIPTION_RATE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_tenant_invoice_validated_data(validated_data):
    if "tenant_subscription_id" in validated_data:
        tenant_subscription = get_tenant_subscription_by_id_string(validated_data["tenant_subscription_id"])
        if tenant_subscription:
            validated_data["tenant_subscription_id"] = tenant_subscription.id
        else:
            raise CustomAPIException(SUBSCRIPTION_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_bank_detail_id" in validated_data:
        tenant_bank_detail = get_tenant_bank_details_by_id_string(validated_data["tenant_bank_detail_id"])
        if tenant_bank_detail:
            validated_data["tenant_bank_detail_id"] = tenant_bank_detail.id
        else:
            raise CustomAPIException(BANK_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_tenant_invoice_payment_validated_data(validated_data):
    if "invoice_id" in validated_data:
        tenant_invoice = get_tenant_invoice_by_id_string(validated_data["invoice_id"])
        if tenant_invoice:
            validated_data["invoice_id"] = tenant_invoice.id
        else:
            raise CustomAPIException(INVOICE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    return validated_data
