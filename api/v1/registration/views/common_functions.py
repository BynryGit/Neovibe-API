from rest_framework import status
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.country import get_country_by_id_string
from v1.commonapp.models.premises import get_premise_by_id_string
from v1.commonapp.models.state import get_state_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.commonapp.models.sub_module import get_sub_module_by_key
from v1.commonapp.models.transition_configuration import TransitionConfiguration, TRANSITION_CHANNEL_DICT, \
    is_transition_configuration_exists
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.views.logger import logger
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string
from v1.consumer.models.consumer_ownership import get_consumer_ownership_by_id_string
from v1.consumer.models.consumer_scheme_master import get_scheme_by_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.consumer.models.source_type import get_source_type_by_id_string
from v1.consumer.signals.signals import after_registration_approved
from v1.payment.models.payment import get_payment_by_id_string
from v1.registration.models.registration_type import get_registration_type_by_id_string
from v1.registration.signals.signals import registration_approved
from v1.registration.views.notifications import registration_email_to_consumer
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.utility.models.utility_services_number_format import *
from v1.registration.models import registrations
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.utility.models.utility_product import get_utility_product_by_id_string
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat


def is_data_verified(request):
    return True


# Function for converting id_strings to id's
def set_registration_validated_data(validated_data):
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
    return validated_data


# Function for generating registration number aaccording to utility
def generate_registration_no(registration):
    try:
        format_obj = UtilityServiceNumberFormat.objects.get(tenant=registration.tenant, utility=registration.utility,
                                                            sub_module_id=get_sub_module_by_key("CONSUMER_OPS_REGISTRATION"))
        print("==========",format_obj)                                                            
        # format_obj = UtilityServiceNumberFormat.objects.get(tenant=registration.tenant, utility=registration.utility,
        #                                                     sub_module_id=get_sub_module_by_key("REGISTRATION"))
        if format_obj.is_prefix:
            registration_no = format_obj.prefix + str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        else:
            registration_no = str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        return registration_no
    except Exception as e:
        print("@@@@@@@@", e)
        raise CustomAPIException("Registration no generation failed.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Function for performing registration transition events
def perform_events(next_state, registration, transition_object):
    try:
        if is_transition_configuration_exists(transition_object, next_state, registration.utility):
            transition_objs = TransitionConfiguration.objects.filter(transition_object=transition_object,
                                                                     transition_state=next_state,
                                                                     utility=registration.utility, is_active=True)
            for transition_obj in transition_objs:
                if transition_obj.channel == TRANSITION_CHANNEL_DICT['EMAIL']:
                    registration_email_to_consumer(registration.id, transition_obj.id)
                if transition_obj.channel == TRANSITION_CHANNEL_DICT['SMS']:
                    pass
                if transition_obj.channel == TRANSITION_CHANNEL_DICT['WHATSAPP']:
                    pass
        else:
            pass
    except Exception as e:
        logger().log(e, 'LOW', module='Consumer Ops', sub_module='Registrations', registration=registration.id)
        pass


# Function for performing registration triggers
def perform_signals(next_state, registration):
    try:
        if next_state == registrations.REGISTRATION_DICT['APPROVED']:
            registration_approved.connect(after_registration_approved)
            registration_approved.send(registration)
    except Exception as e:
        raise CustomAPIException("Registration transition failed", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def set_registration_type_validated_data(validated_data):
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
    if "utility_product_id" in validated_data:
        utility_product = get_utility_product_by_id_string(validated_data["utility_product_id"])
        if utility_product:
            validated_data["utility_product_id"] = utility_product.id
        else:
            raise CustomAPIException("Utility Product not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data

def set_registration_subtype_validated_data(validated_data):
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
            raise CustomAPIException("Registration not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data

