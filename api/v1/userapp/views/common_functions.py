import traceback

import jwt
from django.contrib.auth import authenticate
from django.db.models import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from api.settings import SECRET_KEY
from v1.userapp.models.role import Role

from v1.commonapp.models.department import Department
from v1.commonapp.models.form_factor import FormFactor
from v1.userapp.models.role_privilege import RolePrivilege
from v1.userapp.models.role_sub_type import RoleSubType
from v1.userapp.models.role_type import RoleType
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
            request.data['department'] and request.data['module'] and request.data['Sub_module'] and \
            request.data['privilege']:
        return False
    else:
        return True


@transaction.atomic
def add_basic_registration_details(request, user, sid):
    registration = ""
    try:
        registration = Registration()
        if "first_name" in request.data:
            registration.first_name = request.data["first_name"]
        if "middle_name" in request.data:
            registration.middle_name = request.data["middle_name"]
        if "last_name" in request.data:
            registration.last_name = request.data["last_name"]
        if "email_id" in request.data:
            registration.email_id = request.data["email_id"]
        if "phone_mobile" in request.data:
            registration.phone_mobile = request.data["phone_mobile"]
        if "phone_landline" in request.data:
            registration.phone_landline = request.data["phone_landline"]
        if "address_line_1" in request.data:
            registration.address_line_1 = request.data["address_line_1"]
        if "street" in request.data:
            registration.street = request.data["street"]
        if "zipcode" in request.data:
            registration.zipcode = request.data["zipcode"]
        if "is_vip" in request.data:
            registration.is_vip = True if request.data["is_vip"] == '1' else False
        if "connectivity" in request.data:
            registration.connectivity = True if request.data["connectivity"] == '1' else False
        if "registration_date" in request.data:
            registration.registration_date = datetime.strptime(request.data["registration_date"],INPUT_DATE_FORMAT)
        if "utility_id_string" in request.data:
            utility = get_utility_by_id_string(request.data["utility_id_string"])
            registration.utility = utility
        if "registration_type_id_string" in request.data:
            registration_type = get_registration_type_by_id_string(request.data["registration_type_id_string"])
            registration.registration_type_id = registration_type.id
        if "status_id_string" in request.data:
            registration_status = get_registration_status_by_id_string(request.data["status_id_string"])
            registration.status_id = registration_status.id
        if "country_id_string" in request.data:
            country = get_country_by_id_string(request.data["country_id_string"])
            registration.country_id = country.id
        if "state_id_string" in request.data:
            state = get_state_by_id_string(request.data["state_id_string"])
            registration.state_id = state.id
        if "city_id_string" in request.data:
            city = get_city_by_id_string(request.data["city_id_string"])
            registration.city_id = city.id
        if "area_id_string" in request.data:
            area = get_area_by_id_string(request.data["area_id_string"])
            registration.area_id = area.id
        if "sub_area_id_string" in request.data:
            sub_area = get_sub_area_by_id_string(request.data["sub_area_id_string"])
            registration.sub_area_id = sub_area.id
        if "scheme_id_string" in request.data:
            scheme = get_scheme_by_id_string(request.data["scheme_id_id_string"])
            registration.scheme_id = scheme.id
        if "ownership_id_string" in request.data:
            ownership = get_consumer_ownership_by_id_string(request.data["ownership_id_string"])
            registration.ownership_id = ownership.id
        if "consumer_category_id_string" in request.data:
            consumer_category = get_consumer_category_by_id_string(request.data["consumer_category_id_string"])
            registration.consumer_category_id = consumer_category.id
        if "sub_category_id_string" in request.data:
            sub_category = get_consumer_sub_category_by_id_string(request.data["sub_category_id_string"])
            registration.sub_category_id = sub_category.id
        if "source_id_string" in request.data:
            source = get_source_type_by_id_string(request.data['source_id_string'])
            registration.source_id = source.id
        registration.tenant = user.tenant
        registration.created_by = user.id
        registration.created_date = datetime.now()
        registration.save()
        return registration, True
    except Exception as e:
        print("Exception occured ",str(traceback.print_exc(e)))
        transaction.rollback(sid)
        return registration, False


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
