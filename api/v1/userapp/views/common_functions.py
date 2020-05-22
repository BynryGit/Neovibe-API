import traceback
from datetime import datetime
import jwt
from django.contrib.auth import authenticate
from api.settings import SECRET_KEY
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.department import get_department_by_id_string
from v1.commonapp.models.document_sub_type import get_document_sub_type_by_id_string
from v1.commonapp.models.document_type import get_document_type_by_id_string
from v1.commonapp.models.form_factor import get_form_factor_by_id_string
from v1.commonapp.models.module import get_module_by_id_string
from v1.commonapp.models.service_type import get_service_type_by_id_string
from v1.commonapp.models.sub_module import get_sub_module_by_id_string
from v1.userapp.models.privilege import get_privilege_by_id_string
from v1.userapp.models.role_sub_type import get_role_sub_type_by_id_string
from v1.userapp.models.role_type import get_role_type_by_id_string
from v1.userapp.models.user_bank_detail import get_bank_by_id_string
from v1.userapp.models.user_master import UserDetail, get_user_by_username, get_user_by_id_string
from v1.userapp.models.role import get_role_by_id_string
from v1.userapp.models.user_status import get_user_status_by_id_string
from v1.userapp.models.user_sub_type import get_user_sub_type_by_id_string
from v1.userapp.models.user_token import UserToken, get_token_by_user_id
from v1.userapp.models.user_type import get_user_type_by_id_string



# Check only mandatory fields for role api
def is_role_data_verified(request):
    return True


def is_role_privilege_data_verified(request):
    return True


def is_user_role_data_verified(request):
    return True


def is_user_note_data_verified(request):
    return True


def is_user_data_verified(request):
    return True


def is_bank_data_verified(request):
    return True


def is_document_data_verified(request):
    return True


def is_note_data_verified(request):
    return True


def is_privilege_data_verified(request):
    return True


def set_role_validated_data(validated_data):
    if "type_id" in validated_data:
        type = get_role_type_by_id_string(validated_data["type_id"])
        validated_data["type_id"] = type.id
    if "sub_type_id" in validated_data:
        sub_type = get_role_sub_type_by_id_string(validated_data["sub_type_id"])
        validated_data["sub_type_id"] = sub_type.id
    if "form_factor_id" in validated_data:
        form_factor = get_form_factor_by_id_string(validated_data["form_factor_id"])
        validated_data["form_factor_id"] = form_factor.id
    if "department_id" in validated_data:
        department = get_department_by_id_string(validated_data["department_id"])
        validated_data["department_id"] = department.id
    return validated_data


def set_role_privilege_validated_data(validated_data):
    if "role_id" in validated_data:
        role = get_role_by_id_string(validated_data["role_id"])
        validated_data["role_id"] = role.id
    if "module_id" in validated_data:
        module = get_module_by_id_string(validated_data["module_id"])
        validated_data["module_id"] = module.id
    if "sub_module_id" in validated_data:
        sub_module = get_sub_module_by_id_string(validated_data["sub_module_id"])
        validated_data["sub_module_id"] = sub_module.id
    if "privilege_id" in validated_data:
        privilege = get_privilege_by_id_string(validated_data["privilege_id"])
        validated_data["privilege_id"] = privilege.id
    if "is_active" in validated_data:
        validated_data["is_active"] = bool(validated_data["is_active"])
    return validated_data


def set_user_validated_data(validated_data):
    if "city_id" in validated_data:
        city = get_city_by_id_string(validated_data["city_id"])
        validated_data["city_id"] = city.id
    if "user_type_id" in validated_data:
        user_type = get_user_type_by_id_string(validated_data["user_type_id"])
        validated_data["user_type_id"] = user_type.id
    if "user_subtype_id" in validated_data:
        user_subtype = get_user_sub_type_by_id_string(validated_data["user_subtype_id"])
        validated_data["user_subtype_id"] = user_subtype.id
    if "form_factor_id" in validated_data:
        form_factor = get_form_factor_by_id_string(validated_data["form_factor_id"])
        validated_data["form_factor_id"] = form_factor.id
    if "department_id" in validated_data:
        department = get_department_by_id_string(validated_data["department_id"])
        validated_data["department_id"] = department.id
    if "status_id" in validated_data:
        status = get_user_status_by_id_string(validated_data["status_id"])
        validated_data["status_id"] = status.id
    if "bank_id" in validated_data:
        bank = get_bank_by_id_string(validated_data["bank_id"])
        validated_data["bank_id"] = bank.id
    return validated_data


def set_user_role_validated_data(validated_data):
    if "user_id" in validated_data:
        user = get_user_by_id_string(validated_data["user_id"])
        validated_data["user_id"] = user.id
    if "role_id" in validated_data:
        role = get_role_by_id_string(validated_data["role_id"])
        validated_data["role_id"] = role.id
    if "is_active" in validated_data:
        validated_data["is_active"] = bool(validated_data["is_active"])
    return validated_data


def set_note_validated_data(validated_data):
    if "module_id" in validated_data:
        user = get_module_by_id_string(validated_data["module_id"])
        validated_data["module_id"] = user.id
    if "sub_module_id" in validated_data:
        role = get_sub_module_by_id_string(validated_data["sub_module_id"])
        validated_data["sub_module_id"] = role.id
    if "service_type_id" in validated_data:
        user = get_service_type_by_id_string(validated_data["service_type_id"])
        validated_data["service_type_id"] = user.id
    if "identification_id" in validated_data:
        user = get_user_by_id_string(validated_data["identification_id"])
        validated_data["identification_id"] = user.id
    return validated_data


def set_document_validated_data(validated_data):
    if "module_id" in validated_data:
        user = get_module_by_id_string(validated_data["module_id"])
        validated_data["module_id"] = user.id
    if "sub_module_id" in validated_data:
        role = get_sub_module_by_id_string(validated_data["sub_module_id"])
        validated_data["sub_module_id"] = role.id
    if "document_type_id" in validated_data:
        document_type = get_document_type_by_id_string(validated_data["document_type_id"])
        validated_data["document_type_id"] = document_type.id
    if "document_sub_type_id" in validated_data:
        document_sub_type = get_document_sub_type_by_id_string(validated_data["document_sub_type_id"])
        validated_data["document_sub_type_id"] = document_sub_type.id
    if "identification_id" in validated_data:
        user = get_user_by_id_string(validated_data["identification_id"])
        validated_data["identification_id"] = user.id
    return validated_data


def is_authenticate(validated_data):
    user = authenticate(username=validated_data['username'], password=validated_data['password'])
    if user is not None:
        return user
    else:
        return False


def is_authorized(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        if UserDetail.objects.filter(id_string=str(decoded_token)).exists():
            user_obj = UserDetail.objects.get(id_string=str(decoded_token))
            if UserToken.objects.filter(user=user_obj.id).exists():
                token_obj = UserToken.objects.get(user=user_obj.id)
                if token_obj.token == token:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    except:
        return False


# def check_privilege(user, privilege, activity):
#     if UserRole.objects.filter(id=user.role, is_active=True).exists():
#         role = get_role_by_id(user.role)
#
#         received_privilege = get_privilege_by_id_string(privilege)
#         privileges = UserRole.objects.filter(role=role.id, is_active=True)
#
#         if received_privilege in privileges:
#             return True
#         else:
#             return False
#     else:
#         return False

def login(user):
    try:
        user_obj = get_user_by_username(user.username)
        if UserToken.objects.filter(user_id=user_obj).exists():
            token = get_token_by_user_id(user_obj.id)
            token.delete()
        payload = {'id_string': str(user_obj.id_string)}
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        token_obj = UserToken(user=user_obj.id, token=encoded_jwt)
        token_obj.save()
        return token_obj.token
    except:
        return False