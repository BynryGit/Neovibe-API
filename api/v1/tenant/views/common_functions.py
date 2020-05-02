import traceback
from datetime import datetime
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from api.settings import INPUT_DATE_FORMAT



def get_tenant(request, user):
    total_pages = ''
    page_no = ''
    tenants = ''
    error = ''
    try:
        tenants = tenants.objects.filter(tenant_id=user.tenant_id,
                                                    utility_id__in=user.data_access.all())
        if request.data['city']:
            tenants = tenants.objects.filter(city_id=
                                                         request.data['city'])
        if request.data['area']:
            tenants = tenants.objects.filter(area_id=
                                                         request.data['area'])
        if request.data['subarea']:
            tenants = tenants.objects.filter(subarea_id=
                                                         request.data['subarea'])
        if request.data['status']:
            tenants = tenants.objects.filter(status_id=
                                                         request.data['status'])
        if request.data['search_text'] == '':
            pass
        else:
            tenants = tenants.filter(
                Q(tenant_id__icontains=request.data['search_text']) |
                Q(first_name__icontains=request.data['search_text']))

        if request.data['page_number'] == '':
            paginator = Paginator(tenants,int(request.data['page_size']))
            total_pages = str(paginator.num_pages)
            page_no = '1'
            registrations = paginator.page(1)
        else:
            paginator = Paginator(tenants, int(request.data['page_size']))
            total_pages = str(paginator.num_pages)
            page_no = request.data['page_number']
            tenants = paginator.page(int(page_no))
        return tenants, total_pages, page_no, True, error
    except Exception as e:
        print("Exception occured ",str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return tenants, total_pages, page_no, False, error



