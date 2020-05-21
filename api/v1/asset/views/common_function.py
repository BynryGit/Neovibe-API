__author__ = "Priyanka"

from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.country import get_country_by_id_string
from v1.commonapp.models.state import get_state_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.asset.models.asset_status import get_asset_status_by_id_string

def is_data_verified(request):
    return True

def set_asset_validated_data(validated_data):

    if "category_id" in validated_data:
        consumer_category = get_consumer_category_by_id_string(validated_data["category_id"])
        validated_data["category_id"] = consumer_category.id

    if "sub_category_id" in validated_data:
        sub_category = get_consumer_sub_category_by_id_string(validated_data["sub_category_id"])
        validated_data["sub_category_id"] = sub_category.id

    if "city_id" in validated_data:
        city = get_city_by_id_string(validated_data["city_id"])
        validated_data["city_id"] = city.id

    if "area_id" in validated_data:
        area = get_area_by_id_string(validated_data["area_id"])
        validated_data["area_id"] = area.id

    if "sub_area_id" in validated_data:
        sub_area = get_sub_area_by_id_string(validated_data["sub_area_id"])
        validated_data["sub_area_id"] = sub_area.id

    if "status_id" in validated_data:
        status_id = get_asset_status_by_id_string(validated_data["status_id"])
        validated_data["status_id"] = status_id.id

    return validated_data
