import traceback
from datetime import datetime
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from api.settings import INPUT_DATE_FORMAT
from v1.lookup.models.service_type import get_service_type_by_id_string
from v1.commonapp.models.payment_type import get_payment_type_by_id_string
from v1.supplier.models.supplier_payment import Payment



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

    # only check only mandatory fields
    def is_data_verified(request):  # todo - Black, Null, empty string - ready to use method by Django
        if request.data['name'] == '' and  \
                request.data['mobile_number'] == '' and request.data['email'] == '' and \
               request.data['is_vip'] == '' and request.data['address'] \
                and request.data['street'] == '' and request.data['zipcode'] == '' and \
                request.data['connectivity'] == '':
            return False
        else:
            return True


@transaction.atomic
def save_basic_tenant_details(request, user):
    sid = transaction.savepoint()
    tenant = ""
    error = ''
    try:
        tenant = tenant()
        if request.method == "POST":
            if "short_name" in request.POST:
                tenant.short_name = request.data["short_name"]
            if "name" in request.POST:
                tenant.name = request.data["name"]
            if "phone_no" in request.POST:
                tenant.phone_no = request.data["phone_no"]
            if "mobile_no" in request.POST:
                    tenant.mobile_no = request.data["mobile_no"]
            if "region_id" in request.POST:
                    tenant.region_id = request.data["region_id"]
            if "country_id" in request.POST:
                tenant.country_id = request.data["country_id"]
            if "state_id" in request.POST:
                tenant.state_id = request.data["state_id"]
            if "status_id" in request.POST:
                tenant.status_id = request.data["status_id"]
            if "is_active" in request.POST:
                tenant.is_active = request.data["is_active"]
            tenant.created_by = user.id
            tenant.created_date = datetime.now()
            tenant.save()
        if request.method == "PUT" and "tenant_id_string" in request.PUT:
            tenant = tenant.objects.get(id_string = request.data["tenant_id_string"])
            if "short_name" in request.POST:
                tenant.short_name = request.data["short_name"]
            if "name" in request.POST:
                tenant.name = request.data["name"]
            if "phone_no" in request.POST:
                tenant.phone_no = request.data["phone_no"]
            if "mobile_no" in request.POST:
                tenant.mobile_no = request.data["mobile_no"]
            if "region_id" in request.POST:
                tenant.region_id = request.data["region_id"]
            if "country_id" in request.POST:
                tenant.country_id = request.data["country_id"]
            if "state_id" in request.POST:
                tenant.state_id = request.data["state_id"]
            if "status_id" in request.POST:
                tenant.status_id = request.data["status_id"]
            if "is_active" in request.POST:
                tenant.is_active = request.data["is_active"]
            tenant.updated_by = user.id
            tenant.updated_date = datetime.now()
            tenant.save()
        transaction.savepoint_commit(sid)
        return tenant, True, error
    except Exception as e:
        print("Exception occured ",str(traceback.print_exc(e)))
        transaction.rollback(sid)
        error = str(traceback.print_exc(e))
        return tenant, False, error


def save_payment_details(request, user, tenant):
    try:
        if request.data['payment_details'] == '':
            return True
        else:
            for payment_detail in request.data['payment_details']:
                service_type = get_service_type_by_id_string(payment_detail['service_type_id_string'])
                payment_type = get_payment_type_by_id_string(payment_detail['payment_type_id_string'])
                payment = Payment( # TODO: Payment table is missing
                    tenant = tenant,
                    identification_id = tenant.id,
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






