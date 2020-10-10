import jwt # jwt token library
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