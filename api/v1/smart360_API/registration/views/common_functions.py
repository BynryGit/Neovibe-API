from datetime import datetime

from django.db.models import Q

from api.v1.smart360_API.lookup.models.area import get_area_by_id_string
from api.v1.smart360_API.lookup.models.city import get_city_by_id_string
from api.v1.smart360_API.lookup.models.consumer_category import get_consumer_category_by_id_string
from api.v1.smart360_API.lookup.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from api.v1.smart360_API.lookup.models.country import get_country_by_id_string
from api.v1.smart360_API.lookup.models.registration_type import get_registration_type_by_id_string
from api.v1.smart360_API.lookup.models.source_type import get_source_type_by_id_string
from api.v1.smart360_API.lookup.models.state import get_state_by_id_string
from api.v1.smart360_API.lookup.models.sub_area import get_sub_area_by_id_string
from api.v1.smart360_API.registration.models.registrations import Registration
from django.core.paginator import Paginator



def get_filtered_registrations(request, user):
    total_pages = ''
    page_no = ''
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
    if request.data['page_number'] == '':
        paginator = Paginator(registrations,int(request.data['page_size']))
        total_pages = str(paginator.num_pages)
        page_no = '1'
        registrations = paginator.page(1)
        return registrations,total_pages,page_no
    else:
        paginator = Paginator(registrations, int(request.data['page_size']))
        total_pages = str(paginator.num_pages)
        page_no = request.data['page_no']
        registrations = paginator.page(int(page_no))
        registrations = registrations.filter(
                        Q(registration_no__icontains=request.data['search_text']) |
                        Q(first_name__icontains=request.data['search_text']))
        return registrations, total_pages, page_no


def is_data_verified(request):
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


def save_basic_registration_details(request, user):
    utility = UtilityMaster.objects.get(id_string = request.data['utility']) # Don't have table
    country = get_country_by_id_string(request.data['country'])
    state = get_state_by_id_string(request.data['state'])
    city = get_city_by_id_string(request.data['city'])
    area = get_area_by_id_string(request.data['area'])
    sub_area = get_sub_area_by_id_string(request.data['sub_area'])
    scheme = Scheme.objects.get(id_string=request.data['scheme']) # Don't have table
    ownership = Ownership.objects.get(id_string=request.data['ownership']) # Don't have table
    consumer_category = get_consumer_category_by_id_string(request.data['consumer_category'])
    sub_category = get_consumer_sub_category_by_id_string(request.data['consumer_sub_category'])
    registration_type = get_registration_type_by_id_string(request.data['registration_type'])
    source = get_source_type_by_id_string(request.data['source'])

    registration = Registration(
        tenant = user.tenant,
        utility = utility,
        registration_type_id = registration_type.id,
        first_name = request.data['first_name'],
        middle_name = request.data['middle_name'],
        last_name = request.data['last_name'],
        email_id = request.data['email'],
        phone_mobile = request.data['mobile_number'],
        address_line_1 = request.data['address'],
        street = request.data['street'],
        zipcode = request.data['zipcode'],
        country_id = country.id,
        state_id = state.id,
        city_id = city.id,
        area_id = area.id,
        sub_area_id = sub_area.id,
        scheme_id = scheme.id,
        ownership_id = ownership.id,
        consumer_category_id = consumer_category.id,
        sub_category_id = sub_category.id,
        is_vip = True if request.data['is_vip'] == 'true' else False,
        connectivity = True if request.data['connectivity'] == '1' else False,
        source_id = source.id,
        created_by = user.id,
        created_date = datetime.now()
    ).save()
    registration.registration_no = registration.id
    registration.save()
    return registration


def save_payment_details(request, user, registration):
    try:
        pass
    except Exception as e:
        pass

