import traceback
from datetime import datetime

import jwt
from django.contrib.auth import authenticate
from django.db.models import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from api.settings import SECRET_KEY
from v1.userapp.models.role import Role

from v1.commonapp.models.department import Department, get_department_by_id_string
from v1.commonapp.models.form_factor import FormFactor, get_form_factor_by_id_string
from v1.commonapp.models.module import get_module_by_id_string
from v1.commonapp.models.sub_module import get_sub_module_by_id_string
from v1.userapp.models.role_privilege import RolePrivilege
from v1.userapp.models.role_sub_type import RoleSubType, get_role_sub_type_by_id_string
from v1.userapp.models.role_type import RoleType, get_role_type_by_id_string
from v1.userapp.models.user_master import UserDetail
from v1.userapp.models.user_privilege import UserPrivilege, get_privilege_by_id_string
from v1.userapp.models.user_role import get_role_by_id, UserRole
from v1.userapp.models.user_token import UserToken
from v1.utility.models.utility_master import UtilityMaster


def get_filtered_roles(user, request):
    total_pages = ''
    page_no = ''
    roles = ''
    error = ''
    try:
        roles = UserRole.objects.filter(tenant=user.tenant)

        # fetch records using id_string start
        utility = UtilityMaster.objects.get(id_string=request.data['utility'])
        type = RoleType.objects.get(id_string=request.data['type'])
        sub_type = RoleSubType.objects.get(id_string=request.data['sub_type'])
        form_factor = FormFactor.objects.get(id_string=request.data['form_factor'])
        department = Department.objects.get(id_string=request.data['department'])
        # fetch records using id_string end

        if "utility" in request.data:
            roles = roles.objects.filter(utility_id=utility.id)
        if "type" in request.data:
            roles = roles.objects.filter(type_id=type.id)
        if "sub_type" in request.data:
            roles = roles.objects.filter(sub_type_id=sub_type.id)
        if "form_factor" in request.data:
            roles = roles.objects.filter(form_factor_id=form_factor.id)
        if "department" in request.data:
            roles = roles.objects.filter(department_id=department.id)

        if "search_text" in request.data:
            if request.data['search_text'] == '':
                pass
            else:
                roles = roles.filter(name__icontains=request.data['search_text'])

        if "page_number" in request.data:
            if request.data['page_number'] == '':
                paginator = Paginator(roles, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = '1'
                roles = paginator.page(1)
            else:
                paginator = Paginator(roles, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = request.data['page_number']
                roles = paginator.page(int(page_no))
        return True, roles, total_pages, page_no, error
    except Exception as e:
        print("Exception occurred ", str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return False, roles, total_pages, page_no, error


# Check only mandatory fields
def is_data_verified(request):
    if request.data['role'] and request.data['type'] and request.data['sub_type'] and request.data['form_factor'] and \
            request.data['department']:
        return False
    else:
        return True


@transaction.atomic
def add_basic_role_details(request, user, sid):
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
        return role, True
    except Exception as e:
        print("Exception occured ",str(traceback.print_exc(e)))
        transaction.rollback(sid)
        return role, False


def save_privilege_details(request, user, role, sid):
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
            return True
    except Exception as e:
        transaction.rollback(sid)
        return False


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
        received_activity = get_activity_by_id_string(activity)

        privileges = UserPrivilege.objects.filter(role=role.id, is_active=True)

        if received_privilege in privileges:
            if received_activity.privilege_id == received_privilege.id:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def login(user):
    try:
        user_obj = UserDetail.objects.get(username=user.username)
        if UserToken.objects.filter(user_id=user_obj).exists():
            token = UserToken.objects.get(user_id=user_obj)
            token.delete()
        payload = {'id_string': str(user_obj.id_string)}
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        token_obj = UserToken(user=user_obj.id, token=encoded_jwt)
        token_obj.save()
        return token_obj.token
    except:
        return False
