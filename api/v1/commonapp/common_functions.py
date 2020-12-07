import jwt  # jwt token library
from rest_framework import status

from api.settings import SECRET_KEY
from master.models import get_user_by_id_string, check_user_id_string_exists
from v1.commonapp.models.module import get_module_by_id_string
from v1.commonapp.models.service_type import get_service_type_by_id_string
from v1.commonapp.models.sub_module import get_sub_module_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.views.logger import logger
from v1.userapp.models.user_privilege import check_user_privilege_exists
from v1.userapp.models.user_token import check_token_exists, check_token_exists_for_user
from v1.userapp.models.user_utility import check_user_utility_exists
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.utility.models.utility_module import get_utility_module_by_id_string
from v1.utility.models.utility_sub_module import get_utility_submodule_by_id_string
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.commonapp.models.region import get_region_by_id_string
from v1.commonapp.models.country import get_country_by_id_string
from v1.commonapp.models.state import get_state_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.zone import get_zone_by_id_string
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.utility.models.utility_region import get_utility_region_by_id_string
from v1.commonapp.models.channel import get_channel_by_id_string
from v1.campaign.models.campaign_type import get_campaign_type_by_id_string
from v1.utility.models.utility_channel import get_utility_channel_by_id_string
from v1.utility.models.utility_payment_subtype import get_utility_payment_subtype_by_id_string
from v1.utility.models.utility_payment_type import get_utility_payment_type_by_id_string
from v1.utility.models.utility_payment_mode import get_utility_payment_mode_by_id_string

def get_payload(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms='HS256')
    except:
        return False


def get_user_from_token(token):
    decoded_token = get_payload(token)
    return decoded_token['user_id_string']


def is_token_valid(token):
    try:
        decoded_token = get_payload(token)
        user_obj = get_user_by_id_string(decoded_token['user_id_string'])
        if check_token_exists_for_user(token, user_obj.id):
            return True, user_obj.id_string
        else:
            return False
    except Exception as e:
        logger().log(e, 'ERROR', user='test', name='test')
        return False


def is_authorized(module_id, sub_module_id, privilege_id, user_id):
    return True
    try:
        if check_user_privilege_exists(user_obj.id, module_id, sub_module_id, privilege_id):
            return True
        else:
            return False
    except Exception as e:
        logger().log(e, 'ERROR', user='test', name='test')
        return False


def is_utility(utility_id, user_obj):
    try:
        if check_user_utility_exists(user_obj.id, utility_id):
            return True
        else:
            return False

    except Exception as e:
        logger().log(e, 'ERROR', user='test', name='test')
        return False


def set_note_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            print(utility)
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "module_id" in validated_data:
        module = get_utility_module_by_id_string(validated_data["module_id"])
        if module:
            validated_data["module_id"] = module.id
        else:
            raise CustomAPIException("Module not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "sub_module_id" in validated_data:
        sub_module = get_utility_submodule_by_id_string(validated_data["sub_module_id"])
        if sub_module:
            validated_data["sub_module_id"] = sub_module.id
        else:
            raise CustomAPIException("Sub module not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "service_type_id" in validated_data:
        service_type = get_service_type_by_id_string(validated_data["service_type_id"])
        if service_type:
            validated_data["service_type_id"] = service_type.id
        else:
            raise CustomAPIException("Service type not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_region_validated_data(validated_data):
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
    if "region_id" in validated_data:
        region = get_region_by_id_string(validated_data["region_id"])
        if region:
            validated_data["region_id"] = region.id
        else:
            raise CustomAPIException("Region not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_country_validated_data(validated_data):
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
    if "region_id" in validated_data:
        region = get_utility_region_by_id_string(validated_data["region_id"])
        if region:
            validated_data["region_id"] = region.id
        else:
            raise CustomAPIException("Region not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_state_validated_data(validated_data):
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
    if "region_id" in validated_data:
        region = get_region_by_id_string(validated_data["region_id"])
        if region:
            validated_data["region_id"] = region.id
        else:
            raise CustomAPIException("Region not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "country_id" in validated_data:
        country = get_country_by_id_string(validated_data["country_id"])
        if country:
            validated_data["country_id"] = country.id
        else:
            raise CustomAPIException("Country not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_city_validated_data(validated_data):
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
    if "state_id" in validated_data:
        state = get_state_by_id_string(validated_data["state_id"])
        if state:
            validated_data["state_id"] = state.id
        else:
            raise CustomAPIException("State not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_zone_validated_data(validated_data):
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
    if "city_id" in validated_data:
        city = get_city_by_id_string(validated_data["city_id"])
        if city:
            validated_data["city_id"] = city.id
        else:
            raise CustomAPIException("City not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_area_validated_data(validated_data):
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
    if "zone_id" in validated_data:
        zone = get_zone_by_id_string(validated_data["zone_id"])
        if zone:
            validated_data["zone_id"] = zone.id
        else:
            raise CustomAPIException("Zone not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_subarea_validated_data(validated_data):
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
    if "area_id" in validated_data:
        area = get_area_by_id_string(validated_data["area_id"])
        if area:
            validated_data["area_id"] = area.id
        else:
            raise CustomAPIException("Area not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


def set_premise_validated_data(validated_data):
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
    if "subarea_id" in validated_data:
        subarea = get_sub_area_by_id_string(validated_data["subarea_id"])
        if subarea:
            validated_data["subarea_id"] = subarea.id
        else:
            raise CustomAPIException("SubArea not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data

def set_skill_validated_data(validated_data):
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


def set_frequency_validated_data(validated_data):
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
    if "campaign_type_id" in validated_data:
        campaign_type = get_campaign_type_by_id_string(validated_data["campaign_type_id"])
        if campaign_type:
            validated_data["campaign_type_id"] = campaign_type.id
        else:
            raise CustomAPIException("Campaign Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "channel_type_id" in validated_data:
        channel_type = get_utility_channel_by_id_string(validated_data["channel_type_id"])
        if channel_type:
            validated_data["channel_type_id"] = channel_type.id
        else:
            raise CustomAPIException("Channel Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data

def set_channel_validated_data(validated_data):
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

    if "channel_id" in validated_data:
        channel = get_channel_by_id_string(validated_data["channel_id"])
        if channel:
            validated_data["channel_id"] = channel.id
        else:
            raise CustomAPIException("Channel not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data
    

