import collections
from v1.commonapp.common_functions import validate_user_data
from rest_framework import status
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.premises import get_premise_by_id_string
from v1.commonapp.models.state import get_state_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.commonapp.models.sub_module import get_sub_module_by_key
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string
from v1.consumer.models.consumer_credit_rating import get_consumer_credit_rating_by_id_string
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.consumer.models.consumer_offer_master import get_consumer_offer_master_by_id_string
from v1.consumer.models.consumer_ownership import get_consumer_ownership_by_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.consumer.models.scheme_type import get_scheme_type_by_id_string
from v1.consumer.serializers.consumer_master import ConsumerSerializer
from v1.registration.models import registrations
from v1.utility.models.utility_service_contract_master import get_utility_service_contract_master_by_id_string
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat, \
    UTILITY_SERVICE_NUMBER_ITEM_DICT
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.registration.models.registration_type import get_registration_type_by_id_string
from v1.registration.models.registration_subtype import get_registration_subtype_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.consumer.serializers.consumer_master import ConsumerSerializer
from v1.consumer.models.offer_type import get_offer_type_by_id_string
from v1.consumer.models.offer_sub_type import get_offer_sub_type_by_id_string
from v1.utility.models.utility_module import get_utility_module_by_id_string
from v1.utility.models.utility_sub_module import get_utility_submodule_by_id_string
from v1.utility.models.utility_product import get_utility_product_by_id_string


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
    # if "credit_rating_id" in validated_data:
    #     rating = get_consumer_credit_rating_by_id_string(validated_data["credit_rating_id"])
    #     if rating:
    #         validated_data["credit_rating_id"] = rating.id
    #     else:
    #         raise CustomAPIException("Credit rating not found.", status.HTTP_404_NOT_FOUND)
    return validated_data


# Function for converting id_strings to id's
def set_consumer_offer_detail_validated_data(validated_data):
    if "utility" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility"])
        if utility:
            validated_data["utility"] = utility
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "offer_id" in validated_data:
        offer = get_consumer_offer_master_by_id_string(validated_data["offer_id"])
        if offer:
            validated_data["offer_id"] = offer.id
        else:
            raise CustomAPIException("Consumer offer not found.", status.HTTP_404_NOT_FOUND)
    return validated_data


# Function for converting id_strings to id's
def set_consumer_service_contract_detail_validated_data(validated_data):
    if "premise_id" in validated_data:
        premise = get_premise_by_id_string(validated_data["premise_id"])
        if premise:
            validated_data["premise_id"] = premise.id
        else:
            raise CustomAPIException("Premise not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "service_contract_id" in validated_data:
        utility_service_contract_master = get_utility_service_contract_master_by_id_string(
            validated_data["service_contract_id"])
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


def set_consumer_offer_master_validated_data(validated_data):
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
    if "offer_type_id" in validated_data:
        offer_type = get_offer_type_by_id_string(validated_data["offer_type_id"])
        if offer_type:
            validated_data["offer_type_id"] = offer_type.id
        else:
            raise CustomAPIException("Offer Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "offer_sub_type_id" in validated_data:
        offer_sub_type = get_offer_sub_type_by_id_string(validated_data["offer_sub_type_id"])
        if offer_sub_type:
            validated_data["offer_sub_type_id"] = offer_sub_type.id
        else:
            raise CustomAPIException("Offer Subtype not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "module_id" in validated_data:
        module = get_utility_module_by_id_string(validated_data["module_id"])
        if module:
            validated_data["module_id"] = module.id
        else:
            raise CustomAPIException("Module not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "submodule_id" in validated_data:
        submodule = get_utility_submodule_by_id_string(validated_data["submodule_id"])
        if submodule:
            validated_data["submodule_id"] = submodule.id
        else:
            raise CustomAPIException("Submodule not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_offer_type_validated_data(validated_data):
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


def set_offer_subtype_validated_data(validated_data):
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
    if "offer_type_id" in validated_data:
        offer_type = get_offer_type_by_id_string(validated_data["offer_type_id"])
        if offer_type:
            validated_data["offer_type_id"] = offer_type.id
        else:
            raise CustomAPIException("Offer Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


# Function for generating consumer number according to utility
def generate_consumer_no(consumer):
    try:
        format_obj = UtilityServiceNumberFormat.objects.get(tenant=consumer.tenant, utility=consumer.utility,
                                                            sub_module_id=get_sub_module_by_key("CONSUMER"))
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
        dict['email'] = registration.email_id
        dict['password'] = "pbkdf2_sha256$180000$uzNpPbxCk89A$RVkZS3CagGqM2rjACQprmRJE/Ok769BaaC0rWKdcFWw="
        dict['phone_mobile'] = registration.phone_mobile
        dict['phone_landline'] = registration.phone_landline
        dict['billing_address_line_1'] = registration.billing_address_line_1
        dict['billing_street'] = registration.billing_street
        dict['billing_zipcode'] = registration.billing_zipcode
        dict['billing_state_id'] = registration.billing_state_id
        dict['billing_city_id'] = registration.billing_city_id
        dict['billing_area_id'] = registration.billing_area_id
        dict['billing_sub_area_id'] = registration.billing_sub_area_id
        dict['registration_id'] = registration.id
        dict['premise_id'] = registration.premise_id
        dict['credit_rating_id'] = registration.credit_rating_id
        dict['is_auto_pay'] = registration.is_auto_pay
        dict['is_loan'] = registration.is_loan
        dict['is_upfront_amount'] = registration.is_upfront_amount
        dict['ownership_id'] = registration.ownership_id
        dict['is_address_same'] = registration.is_address_same
        dict['is_vip'] = registration.is_vip
        dict['is_active'] = registration.is_active
        dict['created_by'] = registration.created_by
        dict['updated_by'] = registration.updated_by
        dict['created_date'] = registration.created_date
        dict['updated_date'] = registration.updated_date
        data = collections.OrderedDict(dict)
        consumer = super(ConsumerSerializer, ConsumerSerializer()).create(data)
        consumer.consumer_no = generate_consumer_no(consumer)
        consumer.save()
        return consumer
    except Exception as e:
        print("=====", e)
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
    if "utility_product_id" in validated_data:
        utility_product = get_utility_product_by_id_string(validated_data["utility_product_id"])
        if utility_product:
            validated_data["utility_product_id"] = utility_product.id
        else:
            raise CustomAPIException("Utility Product not found.", status_code=status.HTTP_404_NOT_FOUND)
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
    if "consumer_category_id" in validated_data:
        consumer_category = get_consumer_category_by_id_string(validated_data["consumer_category_id"])
        if consumer_category:
            validated_data["consumer_category_id"] = consumer_category.id
        else:
            raise CustomAPIException("Consumer Category not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "consumer_subcategory_id" in validated_data:
        consumer_subcategory = get_consumer_sub_category_by_id_string(validated_data["consumer_subcategory_id"])
        if consumer_subcategory:
            validated_data["consumer_subcategory_id"] = consumer_subcategory.id
        else:
            raise CustomAPIException("Consumer SubCategory not found", status_code=status.HTTP_404_NOT_FOUND)
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
    if "utility_product_id" in validated_data:
        utility_product = get_utility_product_by_id_string(validated_data["utility_product_id"])
        if utility_product:
            validated_data["utility_product_id"] = utility_product.id
        else:
            raise CustomAPIException("Utility Product not found.", status_code=status.HTTP_404_NOT_FOUND)

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


# Function for converting id_strings to id's
def set_consumer_feedback_validated_data(validated_data):
    if "utility" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility"])
        if utility:
            validated_data["utility"] = utility
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "consumer_id" in validated_data:
        consumer = get_consumer_by_id_string(validated_data["consumer_id"])
        if consumer:
            validated_data["consumer_id"] = consumer.id
        else:
            raise CustomAPIException("Consumer not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data

# Function for generating consumer number according to utility
def generate_transaction_id(consumer):
    try:
        format_obj = UtilityServiceNumberFormat.objects.get(tenant=consumer.tenant, utility=consumer.utility,
                                                            sub_module_id=get_sub_module_by_key("PAYMENT"))
        if format_obj.is_prefix:
            transaction_id = format_obj.prefix + str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        else:
            transaction_id = str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        return transaction_id
    except Exception as e:
        raise CustomAPIException("Transaction id generation failed.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)