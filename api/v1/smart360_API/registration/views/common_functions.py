from django.db.models import Q
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


