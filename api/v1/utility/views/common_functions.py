__author__ = "aki"

from v1.commonapp.models.module import get_module_by_id_string
from v1.commonapp.models.sub_module import get_sub_module_by_id_string
from v1.tenant.models.tenant_city import get_tenant_city_by_id_string
from v1.tenant.models.tenant_country import get_tenant_country_by_id_string
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.tenant.models.tenant_region import get_tenant_region_by_id_string
from v1.tenant.models.tenant_state import get_tenant_state_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.utility.models.utility_product import get_utility_product_by_id_string
from v1.utility.models.utility_status import get_utility_status_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from rest_framework import generics, status
from v1.commonapp.models.sub_module import get_sub_module_by_key
from v1.utility.models.utility_services_number_format import get_item_by_id
from v1.utility.models.utility_sub_module import get_utility_submodule_by_id_string, get_utility_submodule_by_id
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat
from v1.commonapp.models.sub_module import get_sub_module_by_id_string
from v1.utility.models.utility_leave_type import get_utility_leave_by_id_string
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.utility.models.utility_service_contract_template import get_utility_service_contract_template_by_id_string


def set_utility_validated_data(validated_data):
    if "tenant" in validated_data:
        tenant_id_string = (validated_data["tenant"])
        tenant = get_tenant_by_id_string(tenant_id_string.get('id_string'))
        validated_data["tenant"] = tenant.id
    if "region_id" in validated_data:
        region = get_tenant_region_by_id_string(validated_data["region_id"])
        validated_data["region_id"] = region.id
    if "country_id" in validated_data:
        country = get_tenant_country_by_id_string(validated_data["country_id"])
        validated_data["country_id"] = country.id
    if "state_id" in validated_data:
        state = get_tenant_state_by_id_string(validated_data["state_id"])
        validated_data["state_id"] = state.id
    if "city_id" in validated_data:
        city = get_tenant_city_by_id_string(validated_data["city_id"])
        validated_data["city_id"] = city.id
    if "status_id" in validated_data:
        status = get_utility_status_by_id_string(validated_data["status_id"])
        validated_data["status_id"] = status.id
    return validated_data


def set_utility_contract_validated_data(validated_data):
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
    if "consumer_sub_category_id" in validated_data:
        consumer_sub_category = get_consumer_sub_category_by_id_string(validated_data["consumer_sub_category_id"])
        if consumer_sub_category:
            validated_data["consumer_sub_category_id"] = consumer_sub_category.id
        else:
            raise CustomAPIException("Consumer Sub Category not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "service_contract_template_id" in validated_data:
        service_contract_template = get_utility_service_contract_template_by_id_string(
            validated_data["service_contract_template_id"])
        if service_contract_template:
            validated_data["service_contract_template_id"] = service_contract_template.id
        else:
            raise CustomAPIException("Contract Template not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_utility_module_validated_data(validated_data):
    if "tenant" in validated_data:
        tenant_id_string = (validated_data["tenant"])
        tenant = get_tenant_by_id_string(tenant_id_string.get('id_string'))
        validated_data["tenant"] = tenant.id
    if "utility" in validated_data:
        utility_id_string = (validated_data["utility"])
        utility = get_utility_by_id_string(utility_id_string.get('id_string'))
        validated_data["utility"] = utility.id
    if "module_id" in validated_data:
        module = get_module_by_id_string(validated_data["module_id"])
        validated_data["module_id"] = module.id
    return validated_data


def set_utility_submodule_validated_data(validated_data):
    if "tenant" in validated_data:
        tenant_id_string = (validated_data["tenant"])
        tenant = get_tenant_by_id_string(tenant_id_string.get('id_string'))
        validated_data["tenant"] = tenant.id
    if "utility" in validated_data:
        utility_id_string = (validated_data["utility"])
        utility = get_utility_by_id_string(utility_id_string.get('id_string'))
        validated_data["utility"] = utility.id
    if "module_id" in validated_data:
        module = get_module_by_id_string(validated_data["module_id"])
        validated_data["module_id"] = module.id
    if "submodule_id" in validated_data:
        submodule = get_sub_module_by_id_string(validated_data["submodule_id"])
        validated_data["submodule_id"] = submodule.id
    return validated_data


def set_numformat_validated_data(validated_data):
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
    if "sub_module_id" in validated_data:
        submodule_id = get_sub_module_by_id_string(validated_data["sub_module_id"])
        if submodule_id:
            validated_data["sub_module_id"] = submodule_id.id
        else:
            raise CustomAPIException("SubModule Not Found", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_holiday_validated_data(validated_data):
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
    if "holiday_type_id" in validated_data:
        holiday_type = get_utility_leave_by_id_string(validated_data["holiday_type_id"])
        if holiday_type:
            validated_data["holiday_type_id"] = holiday_type.id
        else:
            raise CustomAPIException("Holiday Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_working_hours_validated_data(validated_data):
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


def generate_current_no(user):
    try:
        format_obj = UtilityServiceNumberFormat.objects.get(tenant=user.tenant, utility=user.utility)
        print(format_obj)
        if format_obj.is_prefix == True:
            currentno = format_obj.prefix + str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        else:
            currentno = str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        return currentno
    except Exception:
        raise CustomAPIException("Current No generation failed.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Function for generating userID according to utility
def generate_company_id(user):
    try:
        format_obj = UtilityServiceNumberFormat.objects.get(tenant=user.tenant,
                                                            sub_module_id=get_sub_module_by_key("UTILITY_MASTER"))
        if format_obj.is_prefix == True:
            user_id = format_obj.prefix + str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        else:
            user_id = str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        return user_id
    except Exception as e:
        raise CustomAPIException("Company ID generation failed.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

