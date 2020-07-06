from rest_framework import status

from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.country import get_country_by_id_string
from v1.commonapp.models.state import get_state_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.consumer.models.complaint_status import get_complaint_status_by_id_string
from v1.consumer.models.complaint_sub_type import get_complaint_sub_type_by_id_string
from v1.consumer.models.complaint_type import get_complaint_type_by_id_string
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string
from v1.consumer.models.consumer_scheme_master import get_scheme_by_id_string
from v1.consumer.models.consumer_status import get_consumer_status_by_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.consumer.models.scheme_type import get_scheme_type_by_id_string
from v1.utility.models.utility_service_plan import get_utility_service_plan_by_id_string


def set_consumer_validated_data(validated_data):
    if "area_id" in validated_data:
        area = get_area_by_id_string(validated_data["area_id"])
        if area:
            validated_data["area_id"] = area.id
        else:
            raise CustomAPIException("Area not found.",status_code=status.HTTP_404_NOT_FOUND)
    if "utility_service_plan_id" in validated_data:
        utility_service_plan = get_utility_service_plan_by_id_string(validated_data["utility_service_plan_id"])
        if utility_service_plan:
            validated_data["utility_service_plan_id"] = utility_service_plan.id
        else:
            raise CustomAPIException("Utility service plan not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "consumer_status_id" in validated_data:
        consumer_status = get_consumer_status_by_id_string(validated_data["consumer_status_id"])
        if consumer_status:
            validated_data["consumer_status_id"] = consumer_status.id
        else:
            raise CustomAPIException("Consumer status not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "country_id" in validated_data:
        country = get_country_by_id_string(validated_data["country_id"])
        if country:
            validated_data["country_id"] = country.id
        else:
            raise CustomAPIException("Country not found.", status.HTTP_404_NOT_FOUND)
    if "state_id" in validated_data:
        state = get_state_by_id_string(validated_data["state_id"])
        if state:
            validated_data["state_id"] = state.id
        else:
            raise CustomAPIException("State not found.", status.HTTP_404_NOT_FOUND)
    if "city_id" in validated_data:
        city = get_city_by_id_string(validated_data["city_id"])
        if city:
            validated_data["city_id"] = city.id
        else:
            raise CustomAPIException("City not found.", status.HTTP_404_NOT_FOUND)
    if "scheme_id" in validated_data:
        scheme = get_scheme_by_id_string(validated_data["scheme_id"])
        if scheme:
            validated_data["scheme_id"] = scheme.id
        else:
            raise CustomAPIException("Scheme not found.", status.HTTP_404_NOT_FOUND)
    if "sub_area_id" in validated_data:
        sub_area = get_sub_area_by_id_string(validated_data["sub_area_id"])
        if sub_area:
            validated_data["sub_area_id"] = sub_area.id
        else:
            raise CustomAPIException("Sub area not found.", status.HTTP_404_NOT_FOUND)
    if "consumer_category_id" in validated_data:
        consumer_category = get_consumer_category_by_id_string(validated_data["consumer_category_id"])
        if consumer_category:
            validated_data["consumer_category_id"] = consumer_category.id
        else:
            raise CustomAPIException("Consumer category not found.", status.HTTP_404_NOT_FOUND)
    if "sub_category_id" in validated_data:
        sub_category = get_consumer_sub_category_by_id_string(validated_data["sub_category_id"])
        if sub_category:
            validated_data["sub_category_id"] = sub_category.id
        else:
            raise CustomAPIException("Consumer sub category not found.", status.HTTP_404_NOT_FOUND)
    return validated_data


def set_complaint_validated_data(validated_data):
    if "complaint_type_id" in validated_data:
        complaint_type = get_complaint_type_by_id_string(validated_data["complaint_type_id"])
        if complaint_type:
            validated_data["complaint_type_id"] = complaint_type.id
        else:
            raise CustomAPIException("Complaint type not found.", status.HTTP_404_NOT_FOUND)
    if "complaint_sub_type_id" in validated_data:
        complaint_sub_type = get_complaint_sub_type_by_id_string(validated_data["complaint_sub_type_id"])
        if complaint_sub_type:
            validated_data["complaint_sub_type_id"] = complaint_sub_type.id
        else:
            raise CustomAPIException("Complaint sub type not found.", status.HTTP_404_NOT_FOUND)
    if "complaint_status_id" in validated_data:
        complaint_status = get_complaint_status_by_id_string(validated_data["complaint_status_id"])
        if complaint_status:
            validated_data["complaint_status_id"] = complaint_status.id
        else:
            raise CustomAPIException("Complaint status not found.", status.HTTP_404_NOT_FOUND)
    return validated_data


def set_scheme_validated_data(validated_data):
    if "scheme_type_id" in validated_data:
        scheme_type = get_scheme_type_by_id_string(validated_data["scheme_type_id"])
        validated_data["scheme_type_id"] = scheme_type.id
    return validated_data