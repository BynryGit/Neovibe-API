from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.country import get_country_by_id_string
from v1.commonapp.models.state import get_state_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string
from v1.consumer.models.consumer_scheme_master import get_scheme_by_id_string
from v1.consumer.models.consumer_status import get_consumer_status_by_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.utility.models.utility_service_plan import get_utility_service_plan_by_id_string


def set_validated_data(validated_data):
    if "area_id" in validated_data:
        area = get_area_by_id_string(validated_data["area_id"])
        validated_data["area_id"] = area.id
    if "utility_service_plan_id" in validated_data:
        utility_service_plan = get_utility_service_plan_by_id_string(validated_data["utility_service_plan_id"])
        validated_data["utility_service_plan_id"] = utility_service_plan.id
    if "consumer_status_id" in validated_data:
        consumer_status = get_consumer_status_by_id_string(validated_data["consumer_status_id"])
        validated_data["consumer_status_id"] = consumer_status.id
    if "country_id" in validated_data:
        country = get_country_by_id_string(validated_data["country_id"])
        validated_data["country_id"] = country.id
    if "state_id" in validated_data:
        state = get_state_by_id_string(validated_data["state_id"])
        validated_data["state_id"] = state.id
    if "city_id" in validated_data:
        city = get_city_by_id_string(validated_data["city_id"])
        validated_data["city_id"] = city.id
    if "scheme_id" in validated_data:
        scheme = get_scheme_by_id_string(validated_data["scheme_id"])
        validated_data["scheme_id"] = scheme.id
    if "sub_area_id" in validated_data:
        sub_area = get_sub_area_by_id_string(validated_data["sub_area_id"])
        validated_data["area_id"] = sub_area.id
    if "consumer_category_id" in validated_data:
        consumer_category = get_consumer_category_by_id_string(validated_data["consumer_category_id"])
        validated_data["consumer_category_id"] = consumer_category.id
    if "sub_category_id" in validated_data:
        sub_category = get_consumer_sub_category_by_id_string(validated_data["sub_category_id"])
        validated_data["sub_category_id"] = sub_category.id
    return validated_data