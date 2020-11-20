from rest_framework import status
from master.models import get_user_by_id_string
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.department import get_department_by_id_string
from v1.commonapp.models.document import get_document_by_id_string
from v1.commonapp.models.document_sub_type import get_document_sub_type_by_id_string
from v1.commonapp.models.document_type import get_document_type_by_id_string
from v1.commonapp.models.form_factor import get_form_factor_by_id_string
from v1.commonapp.models.module import get_module_by_id_string
from v1.commonapp.models.notes import get_note_by_id_string
from v1.commonapp.models.service_type import get_service_type_by_id_string
from v1.commonapp.models.skills import get_skill_by_id_string
from v1.commonapp.models.sub_module import get_sub_module_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.supplier.models.supplier import get_supplier_by_id_string
from v1.tenant.models.tenant_bank_details import get_tenant_bank_details_by_id_string
from v1.userapp.models.privilege import get_privilege_by_id_string
from v1.userapp.models.role_sub_type import get_role_sub_type_by_id_string
from v1.userapp.models.role_type import get_role_type_by_id_string
from v1.userapp.models.role import get_role_by_id_string
from v1.userapp.models.user_status import get_user_status_by_id_string
from v1.userapp.models.user_sub_type import get_user_sub_type_by_id_string
from v1.userapp.models.user_type import get_user_type_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string


# For getting ID's from id_string in role API request
def set_role_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "type_id" in validated_data:
        type = get_role_type_by_id_string(validated_data["type_id"])
        if type:
            validated_data["type_id"] = type.id
        else:
            raise CustomAPIException("Role type not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "sub_type_id" in validated_data:
        sub_type = get_role_sub_type_by_id_string(validated_data["sub_type_id"])
        if sub_type:
            validated_data["sub_type_id"] = sub_type.id
        else:
            raise CustomAPIException("Role sub type not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "form_factor_id" in validated_data:
        form_factor = get_form_factor_by_id_string(validated_data["form_factor_id"])
        if form_factor:
            validated_data["form_factor_id"] = form_factor.id
        else:
            raise CustomAPIException("Form factor not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "department_id" in validated_data:
        department = get_department_by_id_string(validated_data["department_id"])
        if department:
            validated_data["department_id"] = department.id
        else:
            raise CustomAPIException("Department not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


# For getting ID's from id_string in privilege API request
def set_role_privilege_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "role_id" in validated_data:
        role = get_role_by_id_string(validated_data["role_id"])
        if role:
            validated_data["role_id"] = role.id
        else:
            raise CustomAPIException("Role not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "module_id" in validated_data:
        module = get_module_by_id_string(validated_data["module_id"])
        if module:
            validated_data["module_id"] = module.id
        else:
            raise CustomAPIException("Module not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "sub_module_id" in validated_data:
        sub_module = get_sub_module_by_id_string(validated_data["sub_module_id"])
        if sub_module:
            validated_data["sub_module_id"] = sub_module.id
        else:
            raise CustomAPIException("Sub module not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "privilege_id" in validated_data:
        privilege = get_privilege_by_id_string(validated_data["privilege_id"])
        if privilege:
            validated_data["privilege_id"] = privilege.id
        else:
            raise CustomAPIException("Privilege not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


# For getting ID's from id_string in user-privilege API request
def set_user_privilege_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "user_id" in validated_data:
        user = get_user_by_id_string(validated_data["user_id"])
        if user:
            validated_data["user_id"] = user.id
        else:
            raise CustomAPIException("User not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "module_id" in validated_data:
        module = get_module_by_id_string(validated_data["module_id"])
        if module:
            validated_data["module_id"] = module.id
        else:
            raise CustomAPIException("Module not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "sub_module_id" in validated_data:
        sub_module = get_sub_module_by_id_string(validated_data["sub_module_id"])
        if sub_module:
            validated_data["sub_module_id"] = sub_module.id
        else:
            raise CustomAPIException("Sub module not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "privilege_id" in validated_data:
        privilege = get_privilege_by_id_string(validated_data["privilege_id"])
        if privilege:
            validated_data["privilege_id"] = privilege.id
        else:
            raise CustomAPIException("Privilege not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


# For getting ID's from id_string in user API request
def set_user_validated_data(validated_data):
    if "city_id" in validated_data:
        city = get_city_by_id_string(validated_data["city_id"])
        if city:
            validated_data["city_id"] = city.id
        else:
            raise CustomAPIException("City not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "user_type_id" in validated_data:
        user_type = get_user_type_by_id_string(validated_data["user_type_id"])
        if user_type:
            validated_data["user_type_id"] = user_type.id
        else:
            raise CustomAPIException("User Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "user_subtype_id" in validated_data:
        user_subtype = get_user_sub_type_by_id_string(validated_data["user_subtype_id"])
        if user_subtype:
            validated_data["user_subtype_id"] = user_subtype.id
        else:
            raise CustomAPIException("User sub type not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "form_factor_id" in validated_data:
        form_factor = get_form_factor_by_id_string(validated_data["form_factor_id"])
        if form_factor:
            validated_data["form_factor_id"] = form_factor.id
        else:
            raise CustomAPIException("Form factor not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "department_id" in validated_data:
        department = get_department_by_id_string(validated_data["department_id"])
        if department:
            validated_data["department_id"] = department.id
        else:
            raise CustomAPIException("Department not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "status_id" in validated_data:
        get_status = get_user_status_by_id_string(validated_data["status_id"])
        if get_status:
            validated_data["status_id"] = get_status.id
        else:
            raise CustomAPIException("Status not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "supplier_id" in validated_data:
        get_supplier = get_supplier_by_id_string(validated_data["supplier_id"])
        if get_supplier:
            validated_data["supplier_id"] = get_supplier.id
        else:
            raise CustomAPIException("Supplier not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


# For getting ID's from id_string in user-role API request
def set_user_role_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "user_id" in validated_data:
        user = get_user_by_id_string(validated_data["user_id"])
        if user:
            validated_data["user_id"] = user.id
        else:
            raise CustomAPIException("User not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "role_id" in validated_data:
        role = get_role_by_id_string(validated_data["role_id"])
        if role:
            validated_data["role_id"] = role.id
        else:
            raise CustomAPIException("Role not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


# For getting ID's from id_string in user-utility API request
def set_user_utility_validated_data(validated_data):
    if "user_id" in validated_data:
        user = get_user_by_id_string(validated_data["user_id"])
        if user:
            validated_data["user_id"] = user.id
        else:
            raise CustomAPIException("User not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


# For getting ID's from id_string in user-area API request
def set_user_area_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "user_id" in validated_data:
        user = get_user_by_id_string(validated_data["user_id"])
        if user:
            validated_data["user_id"] = user.id
        else:
            raise CustomAPIException("User not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "area_id" in validated_data:
        area = get_area_by_id_string(validated_data["area_id"])
        if area:
            validated_data["area_id"] = area.id
        else:
            raise CustomAPIException("Area not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


# For getting ID's from id_string in user-skill API request
def set_user_skill_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "user_id" in validated_data:
        user = get_user_by_id_string(validated_data["user_id"])
        if user:
            validated_data["user_id"] = user.id
        else:
            raise CustomAPIException("User not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "skill_id" in validated_data:
        skill = get_skill_by_id_string(validated_data["skill_id"])
        if skill:
            validated_data["skill_id"] = skill.id
        else:
            raise CustomAPIException("Skill not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


# For getting ID's from id_string in user-bank API request
def set_user_bank_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "user_id" in validated_data:
        user = get_user_by_id_string(validated_data["user_id"])
        if user:
            validated_data["user_id"] = user.id
        else:
            raise CustomAPIException("User not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "bank_id" in validated_data:
        bank = get_tenant_bank_details_by_id_string(validated_data["bank_id"])
        if bank:
            validated_data["bank_id"] = bank.id
        else:
            raise CustomAPIException("Bank not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


# For getting ID's from id_string in user-note API request
def set_note_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "module_id" in validated_data:
        module = get_module_by_id_string(validated_data["module_id"])
        if module:
            validated_data["module_id"] = module.id
        else:
            raise CustomAPIException("Module not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "sub_module_id" in validated_data:
        sub_module = get_sub_module_by_id_string(validated_data["sub_module_id"])
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
    if "identification_id" in validated_data:
        identification = get_user_by_id_string(validated_data["identification_id"])
        if identification:
            validated_data["identification_id"] = identification.id
        else:
            raise CustomAPIException("Identification not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "note_id" in validated_data:
        note = get_note_by_id_string(validated_data["note_id"])
        if note:
            validated_data["note_id"] = note.id
        else:
            raise CustomAPIException("Note not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


# For getting ID's from id_string in user-document API request
def set_document_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "module_id" in validated_data:
        module = get_module_by_id_string(validated_data["module_id"])
        if module:
            validated_data["module_id"] = module.id
        else:
            raise CustomAPIException("Module not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "sub_module_id" in validated_data:
        sub_module = get_sub_module_by_id_string(validated_data["sub_module_id"])
        if sub_module:
            validated_data["sub_module_id"] = sub_module.id
        else:
            raise CustomAPIException("Sub module not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "document_type_id" in validated_data:
        document_type = get_document_type_by_id_string(validated_data["document_type_id"])
        if document_type:
            validated_data["document_type_id"] = document_type.id
        else:
            raise CustomAPIException("Document type not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "document_sub_type_id" in validated_data:
        document_sub_type = get_document_sub_type_by_id_string(validated_data["document_sub_type_id"])
        if document_sub_type:
            validated_data["document_sub_type_id"] = document_sub_type.id
        else:
            raise CustomAPIException("Document Sub type not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "identification_id" in validated_data:
        identification = get_user_by_id_string(validated_data["identification_id"])
        if identification:
            validated_data["identification_id"] = identification.id
        else:
            raise CustomAPIException("Identification not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "document_id" in validated_data:
        document = get_document_by_id_string(validated_data["document_id"])
        if document:
            validated_data["document_id"] = document.id
        else:
            raise CustomAPIException("Document not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


# For getting ID's from id_string in role-sub-type API request
def set_role_sub_type_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "role_type_id" in validated_data:
        type = get_role_type_by_id_string(validated_data["role_type_id"])
        if type:
            validated_data["role_type_id"] = type.id
        else:
            raise CustomAPIException("Role type not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


# For getting ID's from id_string in user-sub-type API request
def set_user_sub_type_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "user_type_id" in validated_data:
        user_type = get_user_type_by_id_string(validated_data["user_type_id"])
        if user_type:
            validated_data["user_type_id"] = user_type.id
        else:
            raise CustomAPIException("User type not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data
