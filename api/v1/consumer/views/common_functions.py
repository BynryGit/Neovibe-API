import collections
from rest_framework import status
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.country import get_country_by_id_string
from v1.commonapp.models.state import get_state_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string
from v1.consumer.models.consumer_scheme_master import get_scheme_by_id_string
from v1.consumer.models.consumer_status import get_consumer_status_by_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.consumer.models.scheme_type import get_scheme_type_by_id_string
from v1.consumer.serializers.consumer import ConsumerSerializer
from v1.registration.models import registrations
from v1.utility.models.utility_service_plan import get_utility_service_plan_by_id_string
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat, \
    UTILITY_SERVICE_NUMBER_ITEM_DICT


# Function for converting id_strings to id's
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


# Function for converting id_strings to id's
def set_scheme_validated_data(validated_data):
    if "scheme_type_id" in validated_data:
        scheme_type = get_scheme_type_by_id_string(validated_data["scheme_type_id"])
        if scheme_type:
            validated_data["scheme_type_id"] = scheme_type.id
        else:
            raise CustomAPIException("Scheme not found.", status.HTTP_404_NOT_FOUND)
    return validated_data


# Function for generating consumer number aaccording to utility
def generate_consumer_no(consumer):
    try:
        format_obj = UtilityServiceNumberFormat.objects.get(tenant = consumer.tenant, utility = consumer.utility,
                                                            item = UTILITY_SERVICE_NUMBER_ITEM_DICT['CONSUMER'])
        if format_obj.is_prefix == True:
            consumer_no = format_obj.prefix + str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        else:
            consumer_no = str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        return consumer_no
    except Exception as e:
        raise CustomAPIException("Consumer_no no generation failed.",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Function for generating consumer registration approved
def create_consumer_after_registration(registration_id):
    try:
        registration = registrations.get_registration_by_id(registration_id)
        dict = {}
        dict['tenant'] = registration.tenant
        dict['utility'] = registration.utility
        dict['first_name'] = registration.first_name
        dict['middle_name'] = registration.middle_name
        dict['last_name'] = registration.last_name
        dict['email_id'] = registration.email_id
        dict['phone_mobile'] = registration.phone_mobile
        dict['phone_landline'] = registration.phone_landline
        dict['address_line_1'] = registration.address_line_1
        dict['street'] = registration.street
        dict['zipcode'] = registration.zipcode
        dict['country_id'] = registration.country_id
        dict['state_id'] = registration.state_id
        dict['city_id'] = registration.city_id
        dict['country_id'] = registration.country_id
        dict['area_id'] = registration.area_id
        dict['sub_area_id'] = registration.sub_area_id
        dict['registration_id'] = registration.id
        data = collections.OrderedDict(dict)
        consumer = super(ConsumerSerializer, ConsumerSerializer()).create(data)
        consumer.consumer_no = generate_consumer_no(consumer)
        consumer.save()
    except Exception as e:
        raise CustomAPIException("Consumer creation failed", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)