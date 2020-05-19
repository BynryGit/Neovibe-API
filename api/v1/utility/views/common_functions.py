__author__ = "aki"

from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.country import get_country_by_id_string
from v1.commonapp.models.region import get_region_by_id_string
from v1.commonapp.models.state import get_state_by_id_string
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.utility.models.utility_status import get_utility_status_by_id_string


def set_utility_validated_data(validated_data):
    if "tenant" in validated_data:
        tenant_id_string = (validated_data["tenant"])
        tenant = get_tenant_by_id_string(tenant_id_string.get('id_string'))
        validated_data["tenant"] = tenant.id
    if "region_id" in validated_data:
        region = get_region_by_id_string(validated_data["region_id"])
        validated_data["region_id"] = region.id
    if "country_id" in validated_data:
        country = get_country_by_id_string(validated_data["country_id"])
        validated_data["country_id"] = country.id
    if "state_id" in validated_data:
        state = get_state_by_id_string(validated_data["state_id"])
        validated_data["state_id"] = state.id
    if "city_id" in validated_data:
        city = get_city_by_id_string(validated_data["city_id"])
        validated_data["city_id"] = city.id
    if "status_id" in validated_data:
        status = get_utility_status_by_id_string(validated_data["status_id"])
        validated_data["status_id"] = status.id
    return validated_data