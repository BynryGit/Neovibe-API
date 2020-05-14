import traceback
from datetime import datetime

import jwt
from django.contrib.auth import authenticate
from django.db.models import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from api.settings import SECRET_KEY
from v1.userapp.models.role import Role

from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.department import Department, get_department_by_id_string
from v1.commonapp.models.document import Document, get_document_by_id_string
from v1.commonapp.models.form_factor import FormFactor, get_form_factor_by_id_string
from v1.commonapp.models.module import get_module_by_id_string
from v1.commonapp.models.notes import Notes, get_note_by_id_string
from v1.commonapp.models.sub_module import get_sub_module_by_id_string
from v1.userapp.models.privilege import filter_privilege_by_id_string
from v1.userapp.models.role_privilege import RolePrivilege, get_role_privilege_by_id_string, \
    get_role_privilege_by_role_id
from v1.userapp.models.role_sub_type import RoleSubType, get_role_sub_type_by_id_string
from v1.userapp.models.role_type import RoleType, get_role_type_by_id_string
from v1.userapp.models.user_bank_detail import get_bank_by_id_string
from v1.userapp.models.user_master import UserDetail, get_user_by_username, get_user_by_id_string
from v1.userapp.models.user_privilege import UserPrivilege, get_privilege_by_id_string
from v1.userapp.models.role import get_role_by_id, UserRole, get_role_by_id_string
from v1.userapp.models.user_status import get_user_status_by_id_string
from v1.userapp.models.user_sub_type import get_user_sub_type_by_id_string
from v1.userapp.models.user_token import UserToken, get_token_by_user_id
from v1.userapp.models.user_type import get_user_type_by_id_string


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


# Check only mandatory fields for role api
def is_role_data_verified(request):
    if request.data['role'] and request.data['type'] and request.data['sub_type'] and request.data['form_factor'] and \
            request.data['department']:
        return True
    else:
        return False


@transaction.atomic
def add_basic_role_details(request, user):
    role = ""
    try:
        role = Role()
        type = get_role_type_by_id_string(request.data["type"])
        sub_type = get_role_sub_type_by_id_string(request.data["type"])
        form_factor = get_form_factor_by_id_string(request.data["form_factor"])
        department = get_department_by_id_string(request.data["department"])

        if "role" in request.data:
            role.role = request.data["role"]
        if "type" in request.data:
            role.type_id = type.id
        if "sub_type" in request.data:
            role.sub_type_id = sub_type.id
        if "form_factor" in request.data:
            role.form_factor_id = form_factor.id
        if "department" in request.data:
            role.department_id = department.id
        role.tenant = user.tenant
        role.created_by = user.id
        role.created_date = datetime.now()
        role.save()
        role.role_ID = role.id
        role.save()
        return role, True, ''
    except Exception as e:
        print("Exception occurred ",str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return role, False, error


def save_privilege_details(request, user, role):
    try:
        if request.data['privilege_details'] == '':
            return True
        else:
            for privilege_detail in request.data['privilege_details']:
                module = get_module_by_id_string(privilege_detail['module_id_string'])
                sub_module = get_sub_module_by_id_string(privilege_detail['sub_module_id_string'])
                privilege = get_privilege_by_id_string(privilege_detail['privilege_id_string'])
                role_privilege = RolePrivilege(
                    tenant = role.tenant,
                    utility = role.utility,
                    role_id = role.id,
                    module_ = module.id,
                    sub_module_id = sub_module.id,
                    privilege_id = privilege.id,
                    created_by = user.id,
                    created_date = datetime.now()
                ).save

            return role, True, ''
    except Exception as e:
        print("Exception occurred ", str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return role, False, error


def save_edited_basic_role_details(request, user):
    role = ''
    try:
        if "role_id_string" in request.data:
            role = get_role_by_id_string(request.data["role_id_string"])
        if "role" in request.data:
            role.role = request.data["role"]
        if "type" in request.data:
            role.type_id = request.data["type"]
        if "sub_type" in request.data:
            role.sub_type_id = request.data["sub_type"]
        if "form_factor" in request.data:
            role.form_factor_id = request.data["form_factor"]
        if "department" in request.data:
            role.department_id = request.data["department"]
        role.updated_by = user.id
        role.updated_date = datetime.now()
        role.save()

        return role, True, ''
    except Exception as e:
        print("Exception occurred ",str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return role, False, error


def save_edited_privilege_details(request, user, role):
    try:
        if request.data['privilege_details'] == '':
            return True
        else:
            for privilege_detail in request.data['privilege_details']:
                role_privilege = get_role_privilege_by_role_id(role.id)
                role_privilege.update(is_active=False)

                role_privilege = get_role_privilege_by_id_string(request.data["role_privilege_id_string"])
                if filter_privilege_by_id_string(privilege_detail['privilege_id_string']):
                    privilege = get_privilege_by_id_string(privilege_detail['privilege_id_string'])
                    role_privilege.privilege_id = privilege.id
                    role_privilege.is_active = True
                    role_privilege.updated_by = user.id
                    role.updated_date = datetime.now()
                else:
                    module = get_module_by_id_string(privilege_detail['module_id_string'])
                    sub_module = get_sub_module_by_id_string(privilege_detail['sub_module_id_string'])
                    privilege = get_privilege_by_id_string(privilege_detail['privilege_id_string'])
                    role_privilege = RolePrivilege(
                        tenant=role.tenant,
                        utility=role.utility,
                        role_id=role.id,
                        module_=module.id,
                        sub_module_id=sub_module.id,
                        privilege_id=privilege.id,
                        created_by=user.id,
                        created_date=datetime.now()
                    ).save

            return role, True, ''
    except Exception as e:
        print("Exception occurred ",str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return role, False, error


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


def check_privilege(user, privilege, activity):
    if Role.objects.filter(id=user.role, is_active=True).exists():
        role = get_role_by_id(user.role)

        received_privilege = get_privilege_by_id_string(privilege)
        privileges = UserPrivilege.objects.filter(role=role.id, is_active=True)

        if received_privilege in privileges:
            return True
        else:
            return False
    else:
        return False


# Check only mandatory fields for user api
def is_user_data_verified(request):
    if request.data['city'] and request.data['user_type'] and request.data['user_subtype'] \
            and request.data['form_factor'] and request.data['department'] and request.data['user_ID'] and \
            request.data['username'] and request.data['first_name'] and request.data['last_name'] and \
            request.data['email'] and request.data['department'] and request.data['utilities'] and \
            request.data['skills'] and request.data['areas']:
        return True
    else:
        return False


@transaction.atomic
def add_basic_user_details(request, user):
    user_detail = ""
    try:
        user_detail = UserDetail()
        city = get_city_by_id_string(request.data["city"])
        type = get_user_type_by_id_string(request.data["user_type"])
        sub_type = get_user_sub_type_by_id_string(request.data["user_subtype"])
        form_factor = get_form_factor_by_id_string(request.data["form_factor"])
        department = get_department_by_id_string(request.data["department"])

        user_detail.city_id = city.id
        user_detail.user_type_id = type.id
        user_detail.user_subtype_id = sub_type.id
        user_detail.form_factor_id = form_factor.id
        user_detail.department_id = department.id
        user_detail.user_ID = request.data["user_ID"]
        user_detail.username = request.data["username"]
        user_detail.first_name = request.data["first_name"]
        user_detail.last_name = request.data["last_name"]
        user_detail.email = request.data["email"]
        user_detail.utilities = request.data["utilities"]
        user_detail.save()

        if "middle_name" in request.data:
            user_detail.middle_name = request.data["middle_name"]
        if "user_image" in request.data:
            user_detail.user_image = request.data["user_image"]
        if "phone_mobile" in request.data:
            user_detail.phone_mobile = request.data["phone_mobile"]
        if "phone_landline" in request.data:
            user_detail.phone_landline = request.data["phone_landline"]
        if "skills" in request.data:
            user_detail.skills = request.data["skills"]
        if "areas" in request.data:
            user_detail.areas = request.data["areas"]
        if "status" in request.data:
            status = get_user_status_by_id_string(request.data["status"])
            user_detail.status_id = status.id
        user_detail.save()

        user_detail.tenant = user.tenant
        user_detail.created_by = user.id
        user_detail.created_date = datetime.now()
        user_detail.save()

        return user_detail, True, ''
    except Exception as e:
        print("Exception occurred ",str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return user_detail, False, error


def save_edited_basic_user_details(request, user):
    user_detail = ''
    try:
        user_detail = user

        user_detail.first_name = request.data["first_name"]
        user_detail.last_name = request.data["last_name"]
        user_detail.email = request.data["email"]
        user_detail.utilities = request.data["utilities"]
        user_detail.save()

        if "middle_name" in request.data:
            user_detail.middle_name = request.data["middle_name"]
        if "user_image" in request.data:
            user_detail.user_image = request.data["user_image"]
        if "phone_mobile" in request.data:
            user_detail.phone_mobile = request.data["phone_mobile"]
        if "phone_landline" in request.data:
            user_detail.phone_landline = request.data["phone_landline"]
        if "skills" in request.data:
            user_detail.skills = request.data["skills"]
        if "areas" in request.data:
            user_detail.areas = request.data["areas"]
        if "status" in request.data:
            status = get_user_status_by_id_string(request.data["status"])
            user_detail.status_id = status.id
        user_detail.save()

        user_detail.updated_by = user.id
        user_detail.updated_date = datetime.now()
        user_detail.save()

        return user_detail, True, ''
    except Exception as e:
        print("Exception occurred ",str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return user_detail, False, error

# Check only mandatory fields for bank api


def is_bank_data_verified(request):
    if request.data['bank']:
        return True
    else:
        return False


def save_bank_details(request, user):
    try:
        if request.data['bank'] == '':
            return True
        else:
            bank = get_bank_by_id_string(request.data['bank'])
            user.bank_detail_id = bank.id
            user.save()

            return user, True, ''
    except Exception as e:
        print("Exception occurred ", str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return user, False, error


def save_edited_bank_details(request, user):
    user_detail = ''
    try:
        if request.data['bank'] == '':
            return True
        else:
            bank = get_bank_by_id_string(request.data['bank'])
            user.bank_detail_id = bank.id
            user.save()

        return user_detail, True, ''
    except Exception as e:
        print("Exception occurred ",str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return user_detail, False, error


# Check only mandatory fields for document api
def is_document_data_verified(request):
    if request.data['module'] and request.data['sub_module'] and request.data['document_type'] and \
            request.data['document_sub_type'] and request.data['name'] and request.data['link']:
        return True
    else:
        return False


def add_user_document(request, user):
    try:
        document = Document()
        document.module_id = request.data["module"]
        document.sub_module_id = request.data["sub_module"]
        document.document_type_id = request.data["document_type"]
        document.document_sub_type_id = request.data["document_sub_type"]
        document.identification_id = user.id
        document.name = request.data["name"]
        document.link = request.data["link"]
        document.save()

        document.tenant = user.tenant
        document.created_by = user.id
        document.created_date = datetime.now()
        document.save()

        return user, True, ''
    except Exception as e:
        user = ''
        print("Exception occurred ", str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return user, False, error


def save_edited_document(request, user):
    try:
        document = get_document_by_id_string(request.data["document"])

        document.name = request.data["name"]
        document.link = request.data["link"]
        document.save()

        document.updated_by = user.id
        document.updated_date = datetime.now()
        document.save()

        return user, True, ''
    except Exception as e:
        user = ''
        print("Exception occurred ",str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return user, False, error


# Check only mandatory fields for document api
def is_note_data_verified(request):
    if request.data['module'] and request.data['sub_module'] and request.data['service_type_id'] and \
            request.data['note_name'] and request.data['note']:
        return True
    else:
        return False


def add_note_document(request, user):
    try:
        note = Notes()

        note.module_id = request.data["module"]
        note.sub_module_id = request.data["sub_module"]
        note.service_type_id = request.data["service_type_id"]
        note.identification_id = user.id
        note.note_name = request.data["note_name"]
        note.note = request.data["note"]
        note.save()

        if "note_color" in request.data:
            note.note_color = request.data["note_color"]
        if "status" in request.data:
            note.status = request.data["status"]
        note.save()

        note.tenant = user.tenant
        note.created_by = user.id
        note.created_date = datetime.now()
        note.save()

        return user, True, ''
    except Exception as e:
        user = ''
        print("Exception occurred ", str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return user, False, error


def save_edited_note(request, user):
    try:
        note = get_note_by_id_string(request.data["note"])

        if 'note_name' in request.data:
            note.note_name = request.data["note_name"]
        if 'note_color' in request.data:
            note.note_color = request.data["note_color"]
        if 'note' in request.data:
            note.note = request.data["note"]
        if 'status' in request.data:
            note.status = request.data["status"]
        note.save()

        note.updated_by = user.id
        note.updated_date = datetime.now()
        note.save()

        return user, True, ''
    except Exception as e:
        user = ''
        print("Exception occurred ",str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return user, False, error


# Check only mandatory fields for user role and privilege api
def is_privilege_data_verified(request):
    if request.data['user'] and request.data['module'] and request.data['sub_module'] and request.data['role'] and \
            request.data['privilege']:
        return True
    else:
        return False


def add_user_privilege(request, user):
    try:
        
        for role in request.data['role']:
            role_id = get_role_by_id_string(role)
            for module in role['module']:
                module_id = get_module_by_id_string(module)
                for sub_module in module['sub_module']:
                    sub_module_id = get_sub_module_by_id_string(sub_module)
                    privilege_id = get_privilege_by_id_string(sub_module['privilege'])

                    user_privilege = UserPrivilege()

                    user_privilege.user_id = request.data["user"]
                    user_privilege.module_id = module_id
                    user_privilege.sub_module_id = sub_module_id
                    user_privilege.role_id = role_id
                    user_privilege.privilege_id = privilege_id
                    user_privilege.save()

                    user_privilege.tenant = user.tenant
                    user_privilege.created_by = user.id
                    user_privilege.created_date = datetime.now()
                    user_privilege.save()

        return user, True, ''
    except Exception as e:
        user = ''
        print("Exception occurred ", str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return user, False, error


def save_edited_privilege(request, user):
    try:
        user_privilege = get_privilege_by_id_string(request.data["privilege"])

        if 'module' in request.data:
            user_privilege.user_id = request.data["module"]
        if 'sub_module' in request.data:
            user_privilege.module_id = request.data["sub_module"]
        if 'role' in request.data:
            user_privilege.role_id = request.data["role"]
        if 'privilege' in request.data:
            user_privilege.privilege_id = request.data["privilege"]
        user_privilege.save()

        user_privilege.updated_by = user.id
        user_privilege.updated_date = datetime.now()
        user_privilege.save()

        return user, True, ''
    except Exception as e:
        user = ''
        print("Exception occurred ",str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return user, False, error
