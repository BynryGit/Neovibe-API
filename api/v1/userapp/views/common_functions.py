from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.department import get_department_by_id_string
from v1.commonapp.models.document_sub_type import get_document_sub_type_by_id_string
from v1.commonapp.models.document_type import get_document_type_by_id_string
from v1.commonapp.models.form_factor import get_form_factor_by_id_string
from v1.commonapp.models.module import get_module_by_id_string
from v1.commonapp.models.service_type import get_service_type_by_id_string
from v1.commonapp.models.skills import get_skill_by_id_string
from v1.commonapp.models.sub_module import get_sub_module_by_id_string
from v1.userapp.models.privilege import get_privilege_by_id_string
from v1.userapp.models.role_sub_type import get_role_sub_type_by_id_string
from v1.userapp.models.role_type import get_role_type_by_id_string
from v1.userapp.models.user_bank_detail import get_bank_by_id_string
from v1.userapp.models.user_master import UserDetail, get_user_by_username, get_user_by_id_string
from v1.userapp.models.role import get_role_by_id_string
from v1.userapp.models.user_status import get_user_status_by_id_string
from v1.userapp.models.user_sub_type import get_user_sub_type_by_id_string
from v1.userapp.models.user_type import get_user_type_by_id_string


# Check only mandatory fields for role api
from v1.utility.models.utility_master import get_utility_by_id_string


def is_role_data_verified(request):
    return True


def is_role_privilege_data_verified(request):
    return True


def is_user_privilege_data_verified(request):
    return True


def is_user_role_data_verified(request):
    return True


def is_user_utility_data_verified(request):
    return True


def is_user_area_data_verified(request):
    return True


def is_user_skill_data_verified(request):
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


def set_user_privilege_validated_data(validated_data):
    if "user_id" in validated_data:
        user = get_user_by_id_string(validated_data["user_id"])
        validated_data["user_id"] = user.id
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


def set_user_utility_validated_data(validated_data):
    if "user_id" in validated_data:
        user = get_user_by_id_string(validated_data["user_id"])
        validated_data["user_id"] = user.id
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        validated_data["utility_id"] = utility.id
    if "is_active" in validated_data:
        validated_data["is_active"] = bool(validated_data["is_active"])
    return validated_data


def set_user_area_validated_data(validated_data):
    if "user_id" in validated_data:
        user = get_user_by_id_string(validated_data["user_id"])
        validated_data["user_id"] = user.id
    if "area_id" in validated_data:
        area = get_area_by_id_string(validated_data["area_id"])
        validated_data["area_id"] = area.id
    if "is_active" in validated_data:
        validated_data["is_active"] = bool(validated_data["is_active"])
    return validated_data


def set_user_skill_validated_data(validated_data):
    if "user_id" in validated_data:
        user = get_user_by_id_string(validated_data["user_id"])
        validated_data["user_id"] = user.id
    if "skill_id" in validated_data:
        skill = get_skill_by_id_string(validated_data["skill_id"])
        validated_data["skill_id"] = skill.id
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


def set_role_sub_type_validated_data(validated_data):
    if "role_type_id" in validated_data:
        type = get_role_type_by_id_string(validated_data["role_type_id"])
        validated_data["role_type_id"] = type.id
    return validated_data


def set_user_sub_type_validated_data(validated_data):
    if "user_type_id" in validated_data:
        user_type = get_user_type_by_id_string(validated_data["user_type_id"])
        validated_data["user_type_id"] = user_type.id
    return validated_data
