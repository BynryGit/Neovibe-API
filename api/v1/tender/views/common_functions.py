__author__ = "aki"

from master.models import get_user_by_id_string
from v1.tenant.models.tenant_city import get_tenant_city_by_id_string
from v1.tenant.models.tenant_country import get_tenant_country_by_id_string
from v1.tenant.models.tenant_state import get_tenant_state_by_id_string
from v1.tender.models.tender_status import get_tender_status_by_id_string
from v1.tender.models.tender_type import get_tender_type_by_id_string
from v1.tender.models.tender_vendor import get_tender_vendor_by_id_string


def set_tender_validated_data(validated_data):
    if "country_id" in validated_data:
        country = get_tenant_country_by_id_string(validated_data["country_id"])
        validated_data["country_id"] = country.id
    if "state_id" in validated_data:
        state = get_tenant_state_by_id_string(validated_data["state_id"])
        validated_data["tenant_state_id"] = state.id
    if "city_id" in validated_data:
        city = get_tenant_city_by_id_string(validated_data["city_id"])
        validated_data["city_id"] = city.id
    if "type_id" in validated_data:
        tenant_type = get_tender_type_by_id_string(validated_data["type_id"])
        validated_data["type_id"] = tenant_type.id
    if "status_id" in validated_data:
        tender_status = get_tender_status_by_id_string(validated_data["status_id"])
        validated_data["status_id"] = tender_status.id
    return validated_data


def set_tender_quotation_validated_data(validated_data):
    if "vendor_id" in validated_data:
        vendor = get_tender_vendor_by_id_string(validated_data["vendor_id"])
        validated_data["vendor_id"] = vendor.id
    return validated_data


def set_tender_vendor_validated_data(validated_data):
    if "vendor_id" in validated_data:
        vendor = get_user_by_id_string(validated_data["vendor_id"])
        validated_data["vendor_id"] = vendor.id
    return validated_data
