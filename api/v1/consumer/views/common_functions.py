import collections
from rest_framework import status
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.premises import get_premise_by_id_string
from v1.commonapp.models.state import get_state_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string
from v1.consumer.models.consumer_credit_rating import get_consumer_credit_rating_by_id_string
from v1.consumer.models.consumer_ownership import get_consumer_ownership_by_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.consumer.models.scheme_type import get_scheme_type_by_id_string
from v1.registration.models import registrations
from v1.utility.models.utility_service_contract_master import get_utility_service_contract_master_by_id_string
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat, \
    UTILITY_SERVICE_NUMBER_ITEM_DICT
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.registration.models.registration_type import get_registration_type_by_id_string
from v1.registration.models.registration_subtype import get_registration_subtype_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.consumer.models.service_type import get_service_type_by_id_string


# Function for converting id_strings to id's
def set_consumer_validated_data(validated_data):
    if "utility" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility"])
        if utility:
            validated_data["utility"] = utility
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "billing_area_id" in validated_data:
        area = get_area_by_id_string(validated_data["billing_area_id"])
        if area:
            validated_data["billing_area_id"] = area.id
        else:
            raise CustomAPIException("Area not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "billing_state_id" in validated_data:
        state = get_state_by_id_string(validated_data["billing_state_id"])
        if state:
            validated_data["billing_state_id"] = state.id
        else:
            raise CustomAPIException("State not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "billing_city_id" in validated_data:
        city = get_city_by_id_string(validated_data["billing_city_id"])
        if city:
            validated_data["billing_city_id"] = city.id
        else:
            raise CustomAPIException("City not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "billing_sub_area_id" in validated_data:
        sub_area = get_sub_area_by_id_string(validated_data["billing_sub_area_id"])
        if sub_area:
            validated_data["billing_sub_area_id"] = sub_area.id
        else:
            raise CustomAPIException("Sub area not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "premise_id" in validated_data:
        premise = get_premise_by_id_string(validated_data["premise_id"])
        if premise:
            validated_data["premise_id"] = premise.id
        else:
            raise CustomAPIException("Premise not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "ownership_id" in validated_data:
        ownership = get_consumer_ownership_by_id_string(validated_data["ownership_id"])
        if ownership:
            validated_data["ownership_id"] = ownership.id
        else:
            raise CustomAPIException("Ownership not found.", status.HTTP_404_NOT_FOUND)
    if "credit_rating_id" in validated_data:
        rating = get_consumer_credit_rating_by_id_string(validated_data["credit_rating_id"])
        if rating:
            validated_data["credit_rating_id"] = rating.id
        else:
            raise CustomAPIException("Credit rating not found.", status.HTTP_404_NOT_FOUND)
    return validated_data


# Function for converting id_strings to id's
def set_consumer_service_contract_detail_validated_data(validated_data):
    if "service_contract_id" in validated_data:
        utility_service_contract_master = get_utility_service_contract_master_by_id_string(validated_data["service_contract_id"])
        if utility_service_contract_master:
            validated_data["service_contract_id"] = utility_service_contract_master.id
        else:
            raise CustomAPIException("Utility service contract not found.", status_code=status.HTTP_404_NOT_FOUND)
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


def set_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


# Function for generating consumer number according to utility
def generate_consumer_no(consumer):
    try:
        format_obj = UtilityServiceNumberFormat.objects.get(tenant=consumer.tenant, utility=consumer.utility,
                                                            item=UTILITY_SERVICE_NUMBER_ITEM_DICT['CONSUMER'])
        if format_obj.is_prefix:
            consumer_no = format_obj.prefix + str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        else:
            consumer_no = str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        return consumer_no
    except Exception as e:
        raise CustomAPIException("Consumer_no no generation failed.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


def set_consumer_category_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_consumer_subcategory_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "category_id" in validated_data:
        category_id = get_consumer_category_by_id_string(validated_data["category_id"])
        if category_id:
            validated_data["category_id"] = category_id.id
        else:
            raise CustomAPIException("Category not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_consumer_ownership_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_consumer_consent_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "registration_type_id" in validated_data:
        registration_type = get_registration_type_by_id_string(validated_data["registration_type_id"])
        if registration_type:
            validated_data["registration_type_id"] = registration_type.id
        else:
            raise CustomAPIException("Registration Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "registration_subtype_id" in validated_data:
        registration_subtype = get_registration_subtype_by_id_string(validated_data["registration_subtype_id"])
        if registration_subtype:
            validated_data["registration_subtype_id"] = registration_subtype.id
        else:
            raise CustomAPIException("Registration SubType not found", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_consumer_support_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "category_id" in validated_data:
        category_id = get_consumer_category_by_id_string(validated_data["category_id"])
        if category_id:
            validated_data["category_id"] = category_id.id
        else:
            raise CustomAPIException("Category not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "subcategory_id" in validated_data:
        subcategory_id = get_consumer_sub_category_by_id_string(validated_data["subcategory_id"])
        if subcategory_id:
            validated_data["subcategory_id"] = subcategory_id.id
        else:
            raise CustomAPIException("SubCategory not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "city_id" in validated_data:
        city = get_city_by_id_string(validated_data["city_id"])
        if city:
            validated_data["city_id"] = city.id
        else:
            raise CustomAPIException("City not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_consumer_faq_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "category_id" in validated_data:
        category_id = get_consumer_category_by_id_string(validated_data["category_id"])
        if category_id:
            validated_data["category_id"] = category_id.id
        else:
            raise CustomAPIException("Category not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "subcategory_id" in validated_data:
        subcategory_id = get_consumer_sub_category_by_id_string(validated_data["subcategory_id"])
        if subcategory_id:
            validated_data["subcategory_id"] = subcategory_id.id
        else:
            raise CustomAPIException("SubCategory not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_service_type_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_service_subtype_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "service_type_id" in validated_data:
        service_type = get_service_type_by_id_string(validated_data["service_type_id"])
        if service_type:
            validated_data["service_type_id"] = service_type.id
        else:
            raise CustomAPIException("Service Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data
