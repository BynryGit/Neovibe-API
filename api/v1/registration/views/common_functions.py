import traceback
from datetime import datetime
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from api.settings import INPUT_DATE_FORMAT
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.consumer_category import get_consumer_category_by_id_string
from v1.commonapp.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.commonapp.models.country import get_country_by_id_string
from v1.commonapp.models.payment_type import get_payment_type_by_id_string
from v1.commonapp.models.state import get_state_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.consumer.models.consumer_ownership import get_consumer_ownership_by_id_string
from v1.consumer.models.consumer_scheme_master import get_scheme_by_id_string
from v1.consumer.models.source_type import get_source_type_by_id_string
from v1.lookup.models.service_type import get_service_type_by_id_string
from v1.registration.models.registration_status import get_registration_status_by_id_string
from v1.registration.models.registration_type import get_registration_type_by_id_string
from v1.registration.models.registrations import Registration, get_registration_by_id_string
from v1.supplier.models.supplier_payment import Payment
from v1.utility.models.utility_master import UtilityMaster, get_utility_by_id_string


def get_filtered_registrations(request, user):
    total_pages = ''
    page_no = ''
    registrations = ''
    error = ''
    try:
        registrations = Registration.objects.filter(tenant_id=user.tenant_id,
                                                    utility_id__in=user.data_access.all())
        if request.data['utillity']:
            registrations = registrations.objects.filter(utility_id=
                                                         request.data['utillity'])
        if request.data['category']:
            registrations = registrations.objects.filter(consumer_category_id=
                                                         request.data['category'])
        if request.data['sub_category']:
            registrations = registrations.objects.filter(sub_category_id=
                                                         request.data['sub_category'])
        if request.data['city']:
            registrations = registrations.objects.filter(city_id=
                                                         request.data['city'])
        if request.data['area']:
            registrations = registrations.objects.filter(area_id=
                                                         request.data['area'])
        if request.data['subarea']:
            registrations = registrations.objects.filter(subarea_id=
                                                         request.data['subarea'])
        if request.data['status']:
            registrations = registrations.objects.filter(status_id=
                                                         request.data['status'])
        if request.data['search_text'] == '':
            pass
        else:
            registrations = registrations.filter(
                Q(registration_no__icontains=request.data['search_text']) |
                Q(first_name__icontains=request.data['search_text']))

        if request.data['page_number'] == '':
            paginator = Paginator(registrations,int(request.data['page_size']))
            total_pages = str(paginator.num_pages)
            page_no = '1'
            registrations = paginator.page(1)
        else:
            paginator = Paginator(registrations, int(request.data['page_size']))
            total_pages = str(paginator.num_pages)
            page_no = request.data['page_number']
            registrations = paginator.page(int(page_no))
        return registrations, total_pages, page_no, True, error
    except Exception as e:
        print("Exception occured ",str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return registrations, total_pages, page_no, False, error


# only check only mandatory fields
def is_data_verified(request): #todo - Black, Null, empty string - ready to use method by Django
    if request.data['first_name'] == '' and request.data['middle_name'] == '' and \
        request.data['last_name'] == '' and request.data['utility'] == '' and \
        request.data['mobile_number'] == '' and request.data['email'] == '' and \
        request.data['consumer_category'] == '' and request.data['consumer_sub_category'] == '' and \
        request.data['ownership'] == '' and request.data['is_vip'] == '' and request.data['address'] \
        and request.data['street'] == '' and request.data['zipcode'] == '' and \
        request.data['connectivity'] == '':
        return False
    else:
        return True


@transaction.atomic
def save_basic_registration_details(request, user):
    sid = transaction.savepoint()
    registration = ""
    error = ''
    try:
        registration = Registration()
        if request.method == "POST":
            if "first_name" in request.POST:
                registration.first_name = request.data["first_name"]
            if "middle_name" in request.POST:
                registration.middle_name = request.data["middle_name"]
            if "last_name" in request.POST:
                registration.last_name = request.data["last_name"]
            if "email_id" in request.POST:
                registration.email_id = request.data["email_id"]
            if "phone_mobile" in request.POST:
                registration.phone_mobile = request.data["phone_mobile"]
            if "phone_landline" in request.POST:
                registration.phone_landline = request.data["phone_landline"]
            if "address_line_1" in request.POST:
                registration.address_line_1 = request.data["address_line_1"]
            if "street" in request.POST:
                registration.street = request.data["street"]
            if "zipcode" in request.POST:
                registration.zipcode = request.data["zipcode"]
            if "is_vip" in request.POST:
                registration.is_vip = True if request.data["is_vip"] == '1' else False
            if "connectivity" in request.POST:
                registration.connectivity = True if request.data["connectivity"] == '1' else False
            if "registration_date" in request.POST:
                registration.registration_date = datetime.strptime(request.data["registration_date"],INPUT_DATE_FORMAT)
            if "utility_id_string" in request.POST:
                utility = get_utility_by_id_string(request.data["utility_id_string"])
                registration.utility = utility
            if "registration_type_id_string" in request.POST:
                registration_type = get_registration_type_by_id_string(request.data["registration_type_id_string"])
                registration.registration_type_id = registration_type.id
            if "status_id_string" in request.POST:
                registration_status = get_registration_status_by_id_string(request.data["status_id_string"])
                registration.status_id = registration_status.id
            if "country_id_string" in request.POST:
                country = get_country_by_id_string(request.data["country"])
                registration.country_id = country.id
            if "state_id_string" in request.POST:
                state = get_state_by_id_string(request.data["state_id_string"])
                registration.state_id = state.id
            if "city_id_string" in request.POST:
                city = get_city_by_id_string(request.data["city_id_string"])
                registration.city_id = city.id
            if "area_id_string" in request.POST:
                area = get_area_by_id_string(request.data["area_id_string"])
                registration.area_id = area.id
            if "sub_area_id_string" in request.POST:
                sub_area = get_sub_area_by_id_string(request.data["sub_area_id_string"])
                registration.sub_area_id = sub_area.id
            if "scheme_id_string" in request.POST:
                scheme = get_scheme_by_id_string(request.data["scheme_id_id_string"])
                registration.scheme_id = scheme.id
            if "ownership_id_string" in request.POST:
                ownership = get_consumer_ownership_by_id_string(request.data["ownership_id_string"])
                registration.ownership_id = ownership.id
            if "consumer_category_id_string" in request.POST:
                consumer_category = get_consumer_category_by_id_string(request.data["consumer_category_id_string"])
                registration.consumer_category_id = consumer_category.id
            if "sub_category_id_string" in request.POST:
                sub_category = get_consumer_sub_category_by_id_string(request.data["sub_category_id_string"])
                registration.sub_category_id = sub_category.id
            if "source_id_string" in request.POST:
                source = get_source_type_by_id_string(request.data['source'])
                registration.source_id = source.id
            registration.created_by = user.id
            registration.created_date = datetime.now()
            registration.save()
        if request.method == "PUT" and "registration_id_string" in request.PUT:
            registration = Registration.objects.get(id_string = request.data["registration_id_string"])
            if "first_name" in request.PUT:
                registration.first_name = request.data["first_name"]
            if "middle_name" in request.PUT:
                registration.middle_name = request.data["middle_name"]
            if "last_name" in request.PUT:
                registration.last_name = request.data["last_name"]
            if "email_id" in request.PUT:
                registration.email_id = request.data["email_id"]
            if "phone_mobile" in request.PUT:
                registration.phone_mobile = request.data["phone_mobile"]
            if "phone_landline" in request.PUT:
                registration.phone_landline = request.data["phone_landline"]
            if "address_line_1" in request.PUT:
                registration.address_line_1 = request.data["address_line_1"]
            if "street" in request.PUT:
                registration.street = request.data["street"]
            if "zipcode" in request.PUT:
                registration.zipcode = request.data["zipcode"]
            if "is_vip" in request.PUT:
                registration.is_vip = True if request.data["is_vip"] == '1' else False
            if "connectivity" in request.PUT:
                registration.connectivity = True if request.data["connectivity"] == '1' else False
            if "registration_date" in request.PUT:
                registration.registration_date = datetime.strptime(request.data["registration_date"],INPUT_DATE_FORMAT)
            if "utility_id_string" in request.PUT:
                utility = get_utility_by_id_string(request.data["utility_id_string"])
                registration.utility = utility
            if "registration_type_id_string" in request.PUT:
                registration_type = get_registration_type_by_id_string(request.data["registration_type_id_string"])
                registration.registration_type_id = registration_type.id
            if "status_id_string" in request.PUT:
                registration_status = get_registration_status_by_id_string(request.data["status_id_string"])
                registration.status_id = registration_status.id
            if "country_id_string" in request.PUT:
                country = get_country_by_id_string(request.data["country"])
                registration.country_id = country.id
            if "state_id_string" in request.PUT:
                state = get_state_by_id_string(request.data["state_id_string"])
                registration.state_id = state.id
            if "city_id_string" in request.PUT:
                city = get_city_by_id_string(request.data["city_id_string"])
                registration.city_id = city.id
            if "area_id_string" in request.PUT:
                area = get_area_by_id_string(request.data["area_id_string"])
                registration.area_id = area.id
            if "sub_area_id_string" in request.PUT:
                sub_area = get_sub_area_by_id_string(request.data["sub_area_id_string"])
                registration.sub_area_id = sub_area.id
            if "scheme_id_string" in request.PUT:
                scheme = get_scheme_by_id_string(request.data["scheme_id_id_string"])
                registration.scheme_id = scheme.id
            if "ownership_id_string" in request.PUT:
                ownership = get_consumer_ownership_by_id_string(request.data["ownership_id_string"])
                registration.ownership_id = ownership.id
            if "consumer_category_id_string" in request.PUT:
                consumer_category = get_consumer_category_by_id_string(request.data["consumer_category_id_string"])
                registration.consumer_category_id = consumer_category.id
            if "sub_category_id_string" in request.PUT:
                sub_category = get_consumer_sub_category_by_id_string(request.data["sub_category_id_string"])
                registration.sub_category_id = sub_category.id
            if "source_id_string" in request.PUT:
                source = get_source_type_by_id_string(request.data['source'])
                registration.source_id = source.id
            registration.updated_by = user.id
            registration.updated_date = datetime.now()
            registration.save()
        transaction.savepoint_commit(sid)
        return registration, True, error
    except Exception as e:
        print("Exception occured ",str(traceback.print_exc(e)))
        transaction.rollback(sid)
        error = str(traceback.print_exc(e))
        return registration, False, error


def save_payment_details(request, user, registration):
    try:
        if request.data['payment_details'] == '':
            return True
        else:
            for payment_detail in request.data['payment_details']:
                service_type = get_service_type_by_id_string(payment_detail['service_type_id_string'])
                payment_type = get_payment_type_by_id_string(payment_detail['payment_type_id_string'])
                payment = Payment( # TODO: Payment table is missing
                    tenant = registration.tenant,
                    utility = registration.utility,
                    identification_id = registration.id,
                    service_type_id = service_type.id,
                    payment_type_id = payment_type.id,
                    paid_amount = payment_detail['amount'],
                    payment_date = datetime.strptime(payment_detail['payment_date'],INPUT_DATE_FORMAT),
                    created_by = user.id,
                    created_date = datetime.now()
                ).save
            return True
    except Exception as e:
        return False




