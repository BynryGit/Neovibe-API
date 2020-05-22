import traceback
from datetime import datetime
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from api.settings import INPUT_DATE_FORMAT
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.country import get_country_by_id_string
from v1.commonapp.models.service_type import get_service_type_by_id_string
from v1.commonapp.models.state import get_state_by_id_string
from v1.payment.models.payment_type import get_payment_type_by_id_string
from v1.supplier.models.supplier_payment import Payment
from v1.tenant.models.tenant_module import get_tenant_module_by_id_string
from v1.tenant.models.tenant_status import get_tenant_status_by_id_string
from v1.tenant.models.tenant_sub_module import get_tenant_submodule_by_id
from v1.tenant.models.tenant_subscription_plan import get_subscription_plan_by_id, get_subscription_plan_by_id_string, \
    get_subscription_plan_by_tenant_id_string


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

def get_tenant_subscription_by_tenant_id_string(request, user):
        total_pages = ''
        page_no = ''
        subscription = ''
        error = ''
        try:
            subscription = subscription.objects.filter(tenant_id=user.tenant_id,
                                             utility_id__in=user.data_access.all())
            if request.data['subscription_plan_id']:
                if request.data['subscription_plan_id']:
                    subscription = subscription.objects.filter(subscription_plan_id=
                                                               request.data['subscription_plan_id'])
                if request.data['subscription_frequency_id']:
                    subscription = subscription.objects.filter(subscription_frequency_id=
                                                                   request.data['subscription_frequency_id'])
                if request.data['start_date']:
                     subscription = subscription.objects.filter(start_date=
                                                                       request.data['start_date'])
            if request.data['end_date']:
                subscription = subscription.objects.filter(end_date=
                                                           request.data['end_date'])

            if request.data['validity_id']:
                subscription = subscription.objects.filter(validity_id=
                                                 request.data['validity_id'])
            if request.data['search_text'] == '':
                pass
            else:
                subscription = subscription.filter(
                    Q(tenant_id__icontains=request.data['search_text']) |
                    Q(first_name__icontains=request.data['search_text']))

            if request.data['page_number'] == '':
                paginator = Paginator(subscription, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = '1'
                registrations = paginator.page(1)
            else:
                paginator = Paginator(subscription, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = request.data['page_number']
                subscription = paginator.page(int(page_no))
            return subscription, total_pages, page_no, True, error
        except Exception as e:
            print("Exception occured ", str(traceback.print_exc(e)))
            error = str(traceback.print_exc(e))
            return subscription, total_pages, page_no, False, error

def get_tenant_subscription_plan_by_tenant_id_string(request, user):
        total_pages = ''
        page_no = ''
        subscription_plan = ''
        error = ''
        try:
            subscription_plan = subscription_plan.objects.filter(tenant_id=user.tenant_id,
                                             utility_id__in=user.data_access.all())
            if request.data['subscription_plan_id']:
                subscription_plan = subscription_plan.objects.filter(subscription_plan_id=
                                                 request.data['subscription_plan_id'])
            if request.data['validity_id']:
                subscription_plan = subscription_plan.objects.filter(validity_id=
                                                 request.data['validity_id'])
            if request.data['subscription_frequency_id']:
                subscription_plan = subscription_plan.objects.filter(subscription_frequency_id=
                                                 request.data['subscription_frequency_id'])
                if request.data['subscription_type']:
                    subscription_plan = subscription_plan.objects.filter(subscription_type=
                                                               request.data['subscription_type'])
                if request.data['max_utility']:
                    subscription_plan = subscription_plan.objects.filter(max_utility=
                                                               request.data['max_utility'])
                if request.data['max_user']:
                    subscription_plan = subscription_plan.objects.filter(max_user=
                                                               request.data['max_user'])
                if request.data['max_consumer']:
                    subscription_plan = subscription_plan.objects.filter(max_consumer=
                                                                         request.data['max_consumer'])
                if request.data['max_storage']:
                    subscription_plan = subscription_plan.objects.filter(max_storage=
                                                                         request.data['max_storage'])
                if request.data['search_text'] == '':
                    pass
                else:
                    subscription_plan = subscription_plan.filter(
                        Q(tenant_id__icontains=request.data['search_text']) |
                        Q(first_name__icontains=request.data['search_text']))

            if request.data['page_number'] == '':
                paginator = Paginator(subscription_plan, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = '1'
                subscription_plan = paginator.page(1)
            else:
                paginator = Paginator(subscription_plan, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = request.data['page_number']
                subscription_plan = paginator.page(int(page_no))
            return subscription_plan, total_pages, page_no, True, error
        except Exception as e:
            print("Exception occured ", str(traceback.print_exc(e)))
            error = str(traceback.print_exc(e))
            return subscription_plan, total_pages, page_no, False, error

def get_tenant_subscription_rate_by_tenant_id_string(request, user):
            total_pages = ''
            page_no = ''
            subscription_rate = ''
            error = ''
            try:
                subscription_rate = subscription_rate.objects.filter(tenant_id=user.tenant_id,
                                                                     utility_id__in=user.data_access.all())
                if request.data['subscription_plan_id']:
                    subscription_rate = subscription_rate.objects.filter(subscription_plan_id=
                                                                         request.data['subscription_plan_id'])
                if request.data['base_rate']:
                    subscription_rate = subscription_rate.objects.filter(base_rate=
                                                                         request.data['base_rate'])
                if request.data['currency']:
                    subscription_rate = subscription_rate.objects.filter(currency=
                                                                             request.data['currency'])
                if request.data['region']:
                    subscription_rate = subscription_rate.objects.filter(region=
                                                                             request.data['region'])
                if request.data['country']:
                    subscription_rate = subscription_rate.objects.filter(country=
                                                                             request.data['country'])
                if request.data['is_taxable']:
                    subscription_rate = subscription_rate.objects.filter(is_taxable=
                                                                             request.data['is_taxable'])
                if request.data['tax']:
                    subscription_rate = subscription_rate.objects.filter(tax=
                                                                             request.data['tax'])
                if request.data['effective_date']:
                    subscription_rate = subscription_rate.objects.filter(effective_date=
                                                                             request.data['effective_date'])
                    if request.data['search_text'] == '':
                        pass
                    else:
                        subscription_rate = subscription_rate.filter(
                            Q(tenant_id__icontains=request.data['search_text']) |
                            Q(first_name__icontains=request.data['search_text']))

                if request.data['page_number'] == '':
                    paginator = Paginator(subscription_rate, int(request.data['page_size']))
                    total_pages = str(paginator.num_pages)
                    page_no = '1'
                    subscription_rate = paginator.page(1)
                else:
                    paginator = Paginator(subscription_rate, int(request.data['page_size']))
                    total_pages = str(paginator.num_pages)
                    page_no = request.data['page_number']
                    subscription_rate = paginator.page(int(page_no))
                return subscription_rate, total_pages, page_no, True, error
            except Exception as e:
                print("Exception occured ", str(traceback.print_exc(e)))
                error = str(traceback.print_exc(e))
                return subscription_rate, total_pages, page_no, False, error


def get_tenant_statuses_by_tenant_id_string(request, user):
    total_pages = ''
    page_no = ''
    tenant_status = ''
    error = ''
    try:
        tenant_status = tenant_status.objects.filter(tenant_id=user.tenant_id)
        if request.data['name']:
            tenant_status = tenant_status.objects.filter(name=
                                                                 request.data['name'])
        if request.data['is_active']:
            tenant_status = tenant_status.objects.filter(is_active=
                                                                 request.data['is_active'])
            if request.data['search_text'] == '':
                pass
            else:
                tenant_status = tenant_status.filter(
                    Q(tenant_id__icontains=request.data['search_text']) |
                    Q(first_name__icontains=request.data['search_text']))

        if request.data['page_number'] == '':
            paginator = Paginator(tenant_status, int(request.data['page_size']))
            total_pages = str(paginator.num_pages)
            page_no = '1'
            tenant_status = paginator.page(1)
        else:
            paginator = Paginator(tenant_status, int(request.data['page_size']))
            total_pages = str(paginator.num_pages)
            page_no = request.data['page_number']
            tenant_status = paginator.page(int(page_no))
        return tenant_status, total_pages, page_no, True, error
    except Exception as e:
        print("Exception occured ", str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return tenant_status, total_pages, page_no, False, error

def get_tenant_invoices_by_tenant_id_string(request, user):
        total_pages = ''
        page_no = ''
        tenant_invoices = ''
        error = ''
        try:
            tenant_invoices = tenant_invoices.objects.filter(tenant_id=user.tenant_id)
            if request.data['subscription_id']:
                tenant_invoices = tenant_invoices.objects.filter(subscription_id=
                                                                     request.data['subscription_id'])
            if request.data['tenant_bank_details_id']:
                tenant_invoices = tenant_invoices.objects.filter(tenant_bank_details_id=
                                                                     request.data['tenant_bank_details_id'])
            if request.data['invoice_number']:
                tenant_invoices = tenant_invoices.objects.filter(invoice_number=
                                                                     request.data['invoice_number'])
            if request.data['invoice_date']:
                tenant_invoices = tenant_invoices.objects.filter(invoice_date=
                                                                     request.data['invoice_date'])
            if request.data['invoice_amt']:
                tenant_invoices = tenant_invoices.objects.filter(invoice_amt=
                                                                     request.data['invoice_amt'])
            if request.data['invoice_tax']:
                tenant_invoices = tenant_invoices.objects.filter(invoice_tax=
                                                                     request.data['invoice_tax'])
            if request.data['invoice_url']:
                tenant_invoices = tenant_invoices.objects.filter(invoice_url=
                                                                     request.data['invoice_url'])
            if request.data['contact_name']:
                tenant_invoices = tenant_invoices.objects.filter(invoice_url=
                                                                     request.data['contact_name'])
            if request.data['due_date']:
                tenant_invoices = tenant_invoices.objects.filter(due_date=
                                                                     request.data['due_date'])
            if request.data['contact_no']:
                tenant_invoices = tenant_invoices.objects.filter(contact_no=
                                                                     request.data['contact_no'])
            if request.data['email_id']:
                tenant_invoices = tenant_invoices.objects.filter(email_id=
                                                                     request.data['email_id'])
            if request.data['month']:
                tenant_invoices = tenant_invoices.objects.filter(month=
                                                                     request.data['month'])
            if request.data['billing_address']:
                tenant_invoices = tenant_invoices.objects.filter(billing_address=
                                                                     request.data['billing_address'])
            if request.data['address']:
                tenant_invoices = tenant_invoices.objects.filter(address=
                                                                     request.data['address'])

            if request.data['search_text'] == '':
                pass
            else:
                tenant_invoices = tenant_invoices.filter(
                    Q(tenant_id__icontains=request.data['search_text']) |
                    Q(first_name__icontains=request.data['search_text']))

            if request.data['page_number'] == '':
                paginator = Paginator(tenant_invoices, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = '1'
                tenant_invoices = paginator.page(1)
            else:
                paginator = Paginator(tenant_invoices, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = request.data['page_number']
                tenant_invoices = paginator.page(int(page_no))
            return tenant_invoices, total_pages, page_no, True, error
        except Exception as e:
            print("Exception occured ", str(traceback.print_exc(e)))
            error = str(traceback.print_exc(e))
            return tenant_invoices, total_pages, page_no, False, error

def get_tenant_payment_by_tenant_id_string(request, user):
        total_pages = ''
        page_no = ''
        tenant_payments = ''
        error = ''
        try:
            tenant_payments = tenant_payments.objects.filter(tenant_id=user.tenant_id)
            if request.data['invoice_number']:
                tenant_payments = tenant_payments.objects.filter(invoice_number=
                                                                 request.data['invoice_number'])
            if request.data['payment_method']:
                tenant_payments = tenant_payments.objects.filter(payment_method=
                                                                 request.data['payment_method'])
            if request.data['payment_channel']:
                tenant_payments = tenant_payments.objects.filter(payment_channel=
                                                                 request.data['payment_channel'])
            if request.data['transaction_no']:
                tenant_payments = tenant_payments.objects.filter(transaction_no=
                                                                 request.data['transaction_no'])
            if request.data['transaction_date']:
                tenant_payments = tenant_payments.objects.filter(transaction_date=
                                                                 request.data['transaction_date'])
            if request.data['amount']:
                tenant_payments = tenant_payments.objects.filter(amount=
                                                                 request.data['amount'])
            if request.data['tax_amount']:
                tenant_payments = tenant_payments.objects.filter(tax_amount=
                                                                 request.data['tax_amount'])
            if request.data['currency']:
                tenant_payments = tenant_payments.objects.filter(currency=
                                                                 request.data['currency'])
            if request.data['is_active']:
                tenant_payments = tenant_payments.objects.filter(is_active=
                                                                 request.data['is_active'])
            if request.data['created_by']:
                tenant_payments = tenant_payments.objects.filter(created_by=
                                                                 request.data['created_by'])
            if request.data['updated_by']:
                tenant_payments = tenant_payments.objects.filter(updated_by=
                                                                 request.data['updated_by'])
            if request.data['created_date']:
                tenant_payments = tenant_payments.objects.filter(created_date=
                                                                 request.data['created_date'])
            if request.data['updated_date']:
                tenant_payments = tenant_payments.objects.filter(updated_date=
                                                                 request.data['updated_date'])
            if request.data['search_text'] == '':
                pass
            else:
                tenant_payments = tenant_payments.filter(
                Q(tenant_id__icontains=request.data['search_text']) |
                Q(first_name__icontains=request.data['search_text']))
            if request.data['page_number'] == '':
                paginator = Paginator(tenant_payments, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = '1'
                tenant_payments = paginator.page(1)
            else:
                paginator = Paginator(tenant_payments, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = request.data['page_number']
                tenant_payments = paginator.page(int(page_no))
            return tenant_payments, total_pages, page_no, True, error
        except Exception as e:
            print("Exception occured ", str(traceback.print_exc(e)))
            error = str(traceback.print_exc(e))
            return tenant_payments, total_pages, page_no, False, error

def get_tenant_bank_details_by_tenant_id_string(request, user):
        total_pages = ''
        page_no = ''
        tenant_bank = ''
        error = ''
        try:
            tenant_bank = tenant_bank.objects.filter(tenant_id=user.tenant_id)
            if request.data['bank_name']:
                tenant_bank = tenant_bank.objects.filter(bank_name=
                                                                 request.data['bank_name'])
            if request.data['branch_name']:
                tenant_bank = tenant_bank.objects.filter(branch_name=
                                                                 request.data['branch_name'])
            if request.data['branch_city']:
                tenant_bank = tenant_bank.objects.filter(branch_city=
                                                                 request.data['branch_city'])
            if request.data['account_number']:
                tenant_bank = tenant_bank.objects.filter(account_number=
                                                                 request.data['account_number'])
            if request.data['account_type']:
                tenant_bank = tenant_bank.objects.filter(account_type=
                                                                 request.data['account_type'])
            if request.data['account_name']:
                tenant_bank = tenant_bank.objects.filter(account_name=
                                                                 request.data['account_name'])
            if request.data['ifsc_no']:
                tenant_bank = tenant_bank.objects.filter(ifsc_no=
                                                                 request.data['ifsc_no'])
            if request.data['pan_no']:
                tenant_bank = tenant_bank.objects.filter(pan_no=
                                                                 request.data['pan_no'])
            if request.data['gst_no']:
                tenant_bank = tenant_bank.objects.filter(gst_no=
                                                             request.data['gst_no'])
            if request.data['tax_id_no']:
                 tenant_bank = tenant_bank.objects.filter(tax_id_no=
                                                                 request.data['tax_id_no'])
            if request.data['is_active']:
                tenant_bank = tenant_bank.objects.filter(is_active=
                                                                 request.data['is_active'])
            if request.data['created_by']:
                tenant_bank = tenant_bank.objects.filter(created_by=
                                                                 request.data['created_by'])
            if request.data['updated_by']:
                tenant_bank = tenant_bank.objects.filter(updated_by=
                                                                 request.data['updated_by'])
            if request.data['created_date']:
                tenant_bank = tenant_bank.objects.filter(created_date=
                                                                 request.data['created_date'])
            if request.data['updated_date']:
                tenant_bank = tenant_bank.objects.filter(updated_date=
                                                                 request.data['updated_date'])
            if request.data['search_text'] == '':
                pass
            else:
                tenant_bank = tenant_bank.filter(
                Q(tenant_id__icontains=request.data['search_text']) |
                Q(first_name__icontains=request.data['search_text']))

            if request.data['page_number'] == '':
                paginator = Paginator(tenant_bank, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = '1'
                tenant_bank = paginator.page(1)
            else:
                paginator = Paginator(tenant_bank, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = request.data['page_number']
                tenant_bank = paginator.page(int(page_no))
            return tenant_bank, total_pages, page_no, True, error
        except Exception as e:
            print("Exception occured ", str(traceback.print_exc(e)))
            error = str(traceback.print_exc(e))
            return tenant_bank, total_pages, page_no, False, error

def get_tenant_summary_by_tenant_id_string(request, user):
        total_pages = ''
        page_no = ''
        tenant_summary = ''
        error = ''
        try:
            tenant_summary = tenant_summary.objects.filter(tenant_id=user.tenant_id)
            if request.data['no_of_utilities']:
                tenant_summary = tenant_summary.objects.filter(no_of_utilities=
                                                         request.data['no_of_utilities'])
            if request.data['no_of_users']:
                tenant_summary = tenant_summary.objects.filter(no_of_users=
                                                         request.data['no_of_users'])
            if request.data['no_of_consumers']:
                tenant_summary = tenant_summary.objects.filter(no_of_consumers=
                                                         request.data['no_of_consumers'])
            if request.data['total_no_of_transaction']:
                tenant_summary = tenant_summary.objects.filter(total_no_of_transaction=
                                                         request.data['total_no_of_transaction'])
            if request.data['no_of_cities']:
                tenant_summary = tenant_summary.objects.filter(no_of_cities=
                                                         request.data['no_of_cities'])
            if request.data['no_of_documents']:
                tenant_summary = tenant_summary.objects.filter(no_of_documents=
                                                         request.data['no_of_documents'])
            if request.data['total_storage_in_use']:
                tenant_summary = tenant_summary.objects.filter(total_storage_in_use=
                                                         request.data['total_storage_in_use'])
            if request.data['month']:
                tenant_summary = tenant_summary.objects.filter(month=
                                                         request.data['month'])
            if request.data['is_active']:
                tenant_summary = tenant_summary.objects.filter(is_active=
                                                         request.data['is_active'])
            if request.data['created_by']:
                tenant_summary = tenant_summary.objects.filter(created_by=
                                                         request.data['created_by'])
            if request.data['updated_by']:
                tenant_summary = tenant_summary.objects.filter(updated_by=
                                                         request.data['updated_by'])
            if request.data['created_date']:
                tenant_summary = tenant_summary.objects.filter(created_date=
                                                         request.data['created_date'])
            if request.data['updated_date']:
                tenant_summary = tenant_summary.objects.filter(updated_date=
                                                         request.data['updated_date'])
                if request.data['search_text'] == '':
                    pass
                else:
                    tenant_summary = tenant_summary.filter(
                        Q(tenant_id__icontains=request.data['search_text']) |
                        Q(first_name__icontains=request.data['search_text']))

            if request.data['page_number'] == '':
                paginator = Paginator(tenant_summary, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = '1'
                tenant_summary = paginator.page(1)
            else:
                paginator = Paginator(tenant_summary, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = request.data['page_number']
                tenant_summary = paginator.page(int(page_no))
            return tenant_summary, total_pages, page_no, True, error
        except Exception as e:
            print("Exception occured ", str(traceback.print_exc(e)))
            error = str(traceback.print_exc(e))
            return tenant_summary, total_pages, page_no, False, error

def get_tenant_sub_modules_by_tenant_id_string(request, user):
        total_pages = ''
        page_no = ''
        tenant_sub_modules = ''
        error = ''
        try:
            tenant_sub_modules = tenant_sub_modules.objects.filter(tenant_id=user.tenant_id)
            if request.data['subscription_id']:
                tenant_sub_modules = tenant_sub_modules.objects.filter(subscription_id=
                                                         request.data['subscription_id'])
            if request.data['module_id']:
                tenant_sub_modules = tenant_sub_modules.objects.filter(module_id=
                                                         request.data['module_id'])
            if request.data['sub_module_id']:
                tenant_sub_modules = tenant_sub_modules.objects.filter(sub_module_id=
                                                         request.data['sub_module_id'])
            if request.data['sub_module_name']:
                tenant_sub_modules = tenant_sub_modules.objects.filter(sub_module_name=
                                                         request.data['sub_module_name'])
            if request.data['is_active']:
                tenant_sub_modules = tenant_sub_modules.objects.filter(is_active=
                                                         request.data['is_active'])
            if request.data['created_by']:
                tenant_sub_modules = tenant_sub_modules.objects.filter(created_by=
                                                         request.data['created_by'])
            if request.data['updated_by']:
                tenant_sub_modules = tenant_sub_modules.objects.filter(updated_by=
                                                         request.data['updated_by'])
            if request.data['created_date']:
                tenant_sub_modules = tenant_sub_modules.objects.filter(created_date=
                                                         request.data['created_date'])
            if request.data['updated_date']:
                tenant_sub_modules = tenant_sub_modules.objects.filter(updated_date=
                                                         request.data['updated_date'])
                if request.data['search_text'] == '':
                    pass
                else:
                    tenant_sub_modules = tenant_sub_modules.filter(
                        Q(tenant_id__icontains=request.data['search_text']) |
                        Q(first_name__icontains=request.data['search_text']))

            if request.data['page_number'] == '':
                paginator = Paginator(tenant_sub_modules, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = '1'
                tenant_sub_modules = paginator.page(1)
            else:
                paginator = Paginator(tenant_sub_modules, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = request.data['page_number']
                tenant_sub_modules = paginator.page(int(page_no))
            return tenant_sub_modules, total_pages, page_no, True, error
        except Exception as e:
            print("Exception occured ", str(traceback.print_exc(e)))
            error = str(traceback.print_exc(e))
            return tenant_sub_modules, total_pages, page_no, False, error

def get_tenant_documents_by_tenant_id_string(request, user):
        total_pages = ''
        page_no = ''
        tenant_document = ''
        error = ''
        try:
            tenant_document = tenant_document.objects.filter(tenant_id=user.tenant_id)
            if request.data['document_name']:
                tenant_document = tenant_document.objects.filter(document_name=
                                                         request.data['document_name'])
            if request.data['document_type.py']:
                tenant_document = tenant_document.objects.filter(document_type=
                                                         request.data['document_type.py'])
            if request.data['sub_module_id']:
                tenant_document = tenant_document.objects.filter(sub_module_id=
                                                         request.data['sub_module_id'])
            if request.data['document_extension']:
                tenant_document = tenant_document.objects.filter(document_extension=
                                                         request.data['document_extension'])
            if request.data['document_link']:
                tenant_document = tenant_document.objects.filter(document_link=
                                                               request.data['document_link'])
            if request.data['is_active']:
                tenant_document = tenant_document.objects.filter(is_active=
                                                         request.data['is_active'])
            if request.data['created_by']:
                tenant_document = tenant_document.objects.filter(created_by=
                                                         request.data['created_by'])
            if request.data['updated_by']:
                tenant_document = tenant_document.objects.filter(updated_by=
                                                         request.data['updated_by'])
            if request.data['created_date']:
                tenant_document = tenant_document.objects.filter(created_date=
                                                         request.data['created_date'])
            if request.data['updated_date']:
                tenant_document = tenant_document.objects.filter(updated_date=
                                                         request.data['updated_date'])
                if request.data['search_text'] == '':
                    pass
                else:
                    tenant_document = tenant_document.filter(
                        Q(tenant_id__icontains=request.data['search_text']) |
                        Q(first_name__icontains=request.data['search_text']))

            if request.data['page_number'] == '':
                paginator = Paginator(tenant_document, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = '1'
                registrations = paginator.page(1)
            else:
                paginator = Paginator(tenant_document, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = request.data['page_number']
                tenant_document = paginator.page(int(page_no))
            return tenant_document, total_pages, page_no, True, error
        except Exception as e:
            print("Exception occured ", str(traceback.print_exc(e)))
            error = str(traceback.print_exc(e))
            return tenant_document, total_pages, page_no, False, error

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

@transaction.atomic
def save_basic_subscription_details(request, user):
    sid = transaction.savepoint()
    subscription = ""
    error = ''
    try:
        subscription = subscription()
        if request.method == "POST":
            if "subscription_frequency_id" in request.POST:
                subscription.subscription_frequency_id = request.data["subscription_frequency_id"]
            if "start_date" in request.POST:
                subscription.start_date = request.data["start_date"]
            if "end_date" in request.POST:
                subscription.end_date = request.data["end_date"]
            if "validity_id" in request.POST:
                subscription.validity_id = request.data["validity_id"]
            if "subscription_plan_id" in request.POST:
                subscription.subscription_plan_id = request.data["subscription_plan_id"]
            if "is_active" in request.POST:
                subscription.is_active = request.data["is_active"]
            subscription.created_by = user.id
            subscription.created_date = datetime.now()
            subscription.save()
        if request.method == "PUT" and "tenant_id_string" in request.PUT:
            subscription = subscription.objects.get(id_string = request.data["tenant_id_string"])
            if "subscription_frequency_id" in request.POST:
                subscription.subscription_frequency_id = request.data["subscription_frequency_id"]
            if "start_date" in request.POST:
                subscription.start_date = request.data["start_date"]
            if "end_date" in request.POST:
                subscription.end_date = request.data["end_date"]
            if "validity_id" in request.POST:
                subscription.validity_id = request.data["validity_id"]
            if "subscription_plan_id" in request.POST:
                subscription.subscription_plan_id = request.data["subscription_plan_id"]
            if "is_active" in request.POST:
                subscription.is_active = request.data["is_active"]
            subscription.updated_by = user.id
            subscription.updated_date = datetime.now()
            subscription.save()
        transaction.savepoint_commit(sid)
        return subscription, True, error
    except Exception as e:
        print("Exception occured ",str(traceback.print_exc(e)))
        transaction.rollback(sid)
        error = str(traceback.print_exc(e))
        return subscription, False, error

@transaction.atomic
def save_basic_subscription_plan_details(request, user):
    sid = transaction.savepoint()
    subscription_plan = ""
    error = ''
    try:
        subscription_plan = subscription_plan()
        if request.method == "POST":
            if "subscription_id" in request.POST:
                subscription_plan.subscription_id = request.data["subscription_id"]
            if "short_name" in request.POST:
                subscription_plan.short_name = request.data["short_name"]
            if "subscription_type" in request.POST:
                subscription_plan.subscription_type = request.data["subscription_type"]
            if "description" in request.POST:
               subscription_plan.description = request.data["description"]
            if "max_utility" in request.POST:
                subscription_plan.max_utility = request.data["max_utility"]
            if "max_user" in request.POST:
                subscription_plan.max_user = request.data["max_user"]
            if "max_consumer" in request.POST:
                subscription_plan.max_consumer = request.data["max_consumer"]
            if "max_storage" in request.POST:
                subscription_plan.max_storage = request.data["max_storage"]
            if "is_active" in request.POST:
                subscription_plan.is_active = request.data["is_active"]
            subscription_plan.created_by = user.id
            subscription_plan.created_date = datetime.now()
            subscription_plan.save()
        if request.method == "PUT" and "tenant_id_string" in request.PUT:
            subscription_plan = subscription_plan.objects.get(id_string = request.data["tenant_id_string"])
            if "subscription_id" in request.POST:
                subscription_plan.subscription_id = request.data["subscription_id"]
            if "short_name" in request.POST:
                subscription_plan.short_name = request.data["short_name"]
            if "subscription_type" in request.POST:
                subscription_plan.subscription_type = request.data["subscription_type"]
            if "description" in request.POST:
                subscription_plan.description = request.data["description"]
            if "max_utility" in request.POST:
                subscription_plan.max_utility = request.data["max_utility"]
            if "max_user" in request.POST:
                subscription_plan.max_user = request.data["max_user"]
            if "max_consumer" in request.POST:
                subscription_plan.max_consumer = request.data["max_consumer"]
            if "max_storage" in request.POST:
                subscription_plan.max_storage = request.data["max_storage"]
            if "is_active" in request.POST:
                subscription_plan.is_active = request.data["is_active"]
            subscription_plan.updated_by = user.id
            subscription_plan.updated_date = datetime.now()
            subscription_plan.save()
        transaction.savepoint_commit(sid)
        return subscription_plan, True, error
    except Exception as e:
        print("Exception occured ",str(traceback.print_exc(e)))
        transaction.rollback(sid)
        error = str(traceback.print_exc(e))
        return subscription_plan, False, error


@transaction.atomic
def save_basic_subscription_rate_details(request, user):
    sid = transaction.savepoint()
    subscription_rate = ""
    error = ''
    try:
        subscription_rate = subscription_rate()
        if request.method == "POST":
            if "tenantsubscriptionplan_id" in request.POST:
                subscription_rate.tenantsubscriptionplan_id = request.data["tenantsubscriptionplan_id"]
            if "base_rate" in request.POST:
                subscription_rate.base_rate = request.data["base_rate"]
            if "currency" in request.POST:
                subscription_rate.currency = request.data["currency"]
            if "region" in request.POST:
               subscription_rate.region = request.data["region"]
            if "country" in request.POST:
                subscription_rate.country = request.data["country"]
            if "is_taxable" in request.POST:
                subscription_rate.is_taxable = request.data["is_taxable"]
            if "tax" in request.POST:
                subscription_rate.tax = request.data["tax"]
            if "effective_date" in request.POST:
                subscription_rate.effective_date = request.data["effective_date"]
            if "is_active" in request.POST:
                subscription_rate.is_active = request.data["is_active"]

            subscription_rate.created_by = user.id
            subscription_rate.created_date = datetime.now()
            subscription_rate.save()
        if request.method == "PUT" and "tenant_id_string" in request.PUT:
            subscription_rate = subscription_rate.objects.get(id_string = request.data["tenant_id_string"])
            if "tenantsubscriptionplan_id" in request.POST:
                subscription_rate.tenantsubscriptionplan_id = request.data["tenantsubscriptionplan_id"]
            if "base_rate" in request.POST:
                subscription_rate.base_rate = request.data["base_rate"]
            if "currency" in request.POST:
                subscription_rate.currency = request.data["currency"]
            if "region" in request.POST:
                subscription_rate.region = request.data["region"]
            if "country" in request.POST:
                subscription_rate.country = request.data["country"]
            if "is_taxable" in request.POST:
                subscription_rate.is_taxable = request.data["is_taxable"]
            if "tax" in request.POST:
                subscription_rate.tax = request.data["tax"]
            if "effective_date" in request.POST:
                subscription_rate.effective_date = request.data["effective_date"]
            if "is_active" in request.POST:
                subscription_rate.is_active = request.data["is_active"]

            subscription_rate.updated_by = user.id
            subscription_rate.updated_date = datetime.now()
            subscription_rate.save()
        transaction.savepoint_commit(sid)
        return subscription_rate, True, error
    except Exception as e:
        print("Exception occured ",str(traceback.print_exc(e)))
        transaction.rollback(sid)
        error = str(traceback.print_exc(e))
        return subscription_rate, False, error

@transaction.atomic
def save_basic_tenant_invoices_details(request, user):
    sid = transaction.savepoint()
    tenant_invoices = ""
    error = ''
    try:
        tenant_invoices = tenant_invoices()
        if request.method == "POST":
            if "subscription_id" in request.POST:
                tenant_invoices.subscription_id = request.data["subscription_id"]
            if "tenant_bank_details_id" in request.POST:
                tenant_invoices.tenant_bank_details_id = request.data["tenant_bank_details_id"]
            if "invoice_number" in request.POST:
                tenant_invoices.invoice_number = request.data["invoice_number"]
            if "invoice_date" in request.POST:
                tenant_invoices.invoice_date = request.data["invoice_date"]
            if "invoice_amt" in request.POST:
                tenant_invoices.invoice_amt = request.data["invoice_amt"]
            if "invoice_tax" in request.POST:
                tenant_invoices.invoice_tax = request.data["invoice_tax"]
            if "invoice_url" in request.POST:
                tenant_invoices.invoice_url = request.data["invoice_url"]
            if "due_date" in request.POST:
                tenant_invoices.due_date = request.data["due_date"]
            if "contact_name" in request.POST:
                tenant_invoices.contact_name = request.data["contact_name"]
            if "contact_no" in request.POST:
                tenant_invoices.contact_no = request.data["contact_no"]
            if "email_id" in request.POST:
                tenant_invoices.email_id = request.data["email_id"]
            if "month" in request.POST:
                tenant_invoices.month = request.data["month"]
            if "billing_address" in request.POST:
                tenant_invoices.billing_address = request.data["billing_address"]
            if "address" in request.POST:
                tenant_invoices.address = request.data["address"]
            if "is_active" in request.POST:
                tenant_invoices.is_active = request.data["is_active"]

            tenant_invoices.created_by = user.id
            tenant_invoices.created_date = datetime.now()
            tenant_invoices.save()
        if request.method == "PUT" and "tenant_id_string" in request.PUT:
            tenant_invoices = tenant_invoices.objects.get(id_string = request.data["tenant_id_string"])
            if "subscription_id" in request.POST:
                tenant_invoices.subscription_id = request.data["subscription_id"]
            if "tenant_bank_details_id" in request.POST:
                tenant_invoices.tenant_bank_details_id = request.data["tenant_bank_details_id"]
            if "invoice_number" in request.POST:
                tenant_invoices.invoice_number = request.data["invoice_number"]
            if "invoice_date" in request.POST:
                tenant_invoices.invoice_date = request.data["invoice_date"]
            if "invoice_amt" in request.POST:
                tenant_invoices.invoice_amt = request.data["invoice_amt"]
            if "invoice_tax" in request.POST:
                tenant_invoices.invoice_tax = request.data["invoice_tax"]
            if "invoice_url" in request.POST:
                tenant_invoices.invoice_url = request.data["invoice_url"]
            if "due_date" in request.POST:
                tenant_invoices.due_date = request.data["due_date"]
            if "contact_name" in request.POST:
                tenant_invoices.contact_name = request.data["contact_name"]
            if "contact_no" in request.POST:
                tenant_invoices.contact_no = request.data["contact_no"]
            if "email_id" in request.POST:
                tenant_invoices.email_id = request.data["email_id"]
            if "month" in request.POST:
                tenant_invoices.month = request.data["month"]
            if "billing_address" in request.POST:
                tenant_invoices.billing_address = request.data["billing_address"]
            if "address" in request.POST:
                tenant_invoices.address = request.data["address"]
            if "is_active" in request.POST:
                tenant_invoices.is_active = request.data["is_active"]

            tenant_invoices.updated_by = user.id
            tenant_invoices.updated_date = datetime.now()
            tenant_invoices.save()
        transaction.savepoint_commit(sid)
        return tenant_invoices, True, error
    except Exception as e:
        print("Exception occured ",str(traceback.print_exc(e)))
        transaction.rollback(sid)
        error = str(traceback.print_exc(e))
        return tenant_invoices, False, error


@transaction.atomic
def save_basic_tenant_bank_details(request, user):
    sid = transaction.savepoint()
    tenant_bank = ""
    error = ''
    try:
        tenant_bank = tenant_bank()
        if request.method == "POST":
            if "bank_name" in request.POST:
                tenant_bank.bank_name = request.data["bank_name"]
            if "branch_name" in request.POST:
                tenant_bank.branch_name = request.data["branch_name"]
            if "branch_city" in request.POST:
                tenant_bank.branch_city = request.data["branch_city"]
            if "account_number" in request.POST:
                tenant_bank.account_number = request.data["account_number"]
            if "account_type" in request.POST:
                tenant_bank.account_type = request.data["account_type"]
            if "account_name" in request.POST:
                tenant_bank.account_name = request.data["account_name"]
            if "ifsc_no" in request.POST:
                tenant_bank.ifsc_no = request.data["ifsc_no"]
            if "pan_no" in request.POST:
                tenant_bank.pan_no = request.data["pan_no"]
            if "gst_no" in request.POST:
                tenant_bank.gst_no = request.data["gst_no"]
            if "tax_id_no" in request.POST:
                tenant_bank.tax_id_no = request.data["tax_id_no"]
            if "is_active" in request.POST:
                tenant_bank.is_active = request.data["is_active"]

            tenant_bank.created_by = user.id
            tenant_bank.created_date = datetime.now()
            tenant_bank.save()
        if request.method == "PUT" and "tenant_id_string" in request.PUT:
            tenant_bank = tenant_bank.objects.get(id_string=request.data["tenant_id_string"])
            if "bank_name" in request.POST:
                tenant_bank.bank_name = request.data["bank_name"]
            if "branch_name" in request.POST:
                tenant_bank.branch_name = request.data["branch_name"]
            if "branch_city" in request.POST:
                tenant_bank.branch_city = request.data["branch_city"]
            if "account_number" in request.POST:
                tenant_bank.account_number = request.data["account_number"]
            if "account_type" in request.POST:
                tenant_bank.account_type = request.data["account_type"]
            if "account_name" in request.POST:
                tenant_bank.account_name = request.data["account_name"]
            if "ifsc_no" in request.POST:
                tenant_bank.ifsc_no = request.data["ifsc_no"]
            if "pan_no" in request.POST:
                tenant_bank.pan_no = request.data["pan_no"]
            if "gst_no" in request.POST:
                tenant_bank.gst_no = request.data["gst_no"]
            if "tax_id_no" in request.POST:
                tenant_bank.tax_id_no = request.data["tax_id_no"]
            if "is_active" in request.POST:
                tenant_bank.is_active = request.data["is_active"]

            tenant_bank.updated_by = user.id
            tenant_bank.updated_date = datetime.now()
            tenant_bank.save()
        transaction.savepoint_commit(sid)
        return tenant_bank, True, error
    except Exception as e:
        print("Exception occured ", str(traceback.print_exc(e)))
        transaction.rollback(sid)
        error = str(traceback.print_exc(e))
        return tenant_bank, False, error

@transaction.atomic
def save_basic_tenant_bank_details(request, user):
    sid = transaction.savepoint()
    tenant_bank = ""
    error = ''
    try:
        tenant_bank = tenant_bank()
        if request.method == "POST":
            if "bank_name" in request.POST:
                tenant_bank.bank_name = request.data["bank_name"]
            if "branch_name" in request.POST:
                tenant_bank.branch_name = request.data["branch_name"]
            if "branch_city" in request.POST:
                tenant_bank.branch_city = request.data["branch_city"]
            if "account_number" in request.POST:
                tenant_bank.account_number = request.data["account_number"]
            if "account_type" in request.POST:
                tenant_bank.account_type = request.data["account_type"]
            if "account_name" in request.POST:
                tenant_bank.account_name = request.data["account_name"]
            if "ifsc_no" in request.POST:
                tenant_bank.ifsc_no = request.data["ifsc_no"]
            if "pan_no" in request.POST:
                tenant_bank.pan_no = request.data["pan_no"]
            if "gst_no" in request.POST:
                tenant_bank.gst_no = request.data["gst_no"]
            if "tax_id_no" in request.POST:
                tenant_bank.tax_id_no = request.data["tax_id_no"]
            if "is_active" in request.POST:
                tenant_bank.is_active = request.data["is_active"]

            tenant_bank.created_by = user.id
            tenant_bank.created_date = datetime.now()
            tenant_bank.save()
        if request.method == "PUT" and "tenant_id_string" in request.PUT:
            tenant_bank = tenant_bank.objects.get(id_string=request.data["tenant_id_string"])
            if "bank_name" in request.POST:
                tenant_bank.bank_name = request.data["bank_name"]
            if "branch_name" in request.POST:
                tenant_bank.branch_name = request.data["branch_name"]
            if "branch_city" in request.POST:
                tenant_bank.branch_city = request.data["branch_city"]
            if "account_number" in request.POST:
                tenant_bank.account_number = request.data["account_number"]
            if "account_type" in request.POST:
                tenant_bank.account_type = request.data["account_type"]
            if "account_name" in request.POST:
                tenant_bank.account_name = request.data["account_name"]
            if "ifsc_no" in request.POST:
                tenant_bank.ifsc_no = request.data["ifsc_no"]
            if "pan_no" in request.POST:
                tenant_bank.pan_no = request.data["pan_no"]
            if "gst_no" in request.POST:
                tenant_bank.gst_no = request.data["gst_no"]
            if "tax_id_no" in request.POST:
                tenant_bank.tax_id_no = request.data["tax_id_no"]
            if "is_active" in request.POST:
                tenant_bank.is_active = request.data["is_active"]

            tenant_bank.updated_by = user.id
            tenant_bank.updated_date = datetime.now()
            tenant_bank.save()
        transaction.savepoint_commit(sid)
        return tenant_bank, True, error
    except Exception as e:
        print("Exception occured ", str(traceback.print_exc(e)))
        transaction.rollback(sid)
        error = str(traceback.print_exc(e))
        return tenant_bank, False, error

@transaction.atomic
def save_basic_tenant_document_details(request, user):
        sid = transaction.savepoint()
        tenant_document = ""
        error = ''
        try:
            tenant_document = tenant_document()
            if request.method == "POST":
                if "document_name" in request.POST:
                    tenant_document.document_name = request.data["document_name"]
                if "document_type.py" in request.POST:
                    tenant_document.document_type = request.data["document_type.py"]
                if "sub_module_id" in request.POST:
                    tenant_document.sub_module_id = request.data["sub_module_id"]
                if "document_extension" in request.POST:
                    tenant_document.document_extension = request.data["document_extension"]
                if "document_link" in request.POST:
                    tenant_document.document_link = request.data["document_link"]
                if "is_active" in request.POST:
                    tenant_document.is_active = request.data["is_active"]
                tenant_document.created_by = user.id
                tenant_document.created_date = datetime.now()
                tenant_document.save()
            if request.method == "PUT" and "tenant_id_string" in request.PUT:
                tenant_document = tenant_document.objects.get(id_string=request.data["tenant_id_string"])
                if "document_name" in request.POST:
                    tenant_document.document_name = request.data["document_name"]
                if "document_type.py" in request.POST:
                    tenant_document.document_type = request.data["document_type.py"]
                if "sub_module_id" in request.POST:
                    tenant_document.sub_module_id = request.data["sub_module_id"]
                if "document_extension" in request.POST:
                    tenant_document.document_extension = request.data["document_extension"]
                if "document_link" in request.POST:
                    tenant_document.document_link = request.data["document_link"]
                if "is_active" in request.POST:
                    tenant_document.is_active = request.data["is_active"]

                tenant_document.updated_by = user.id
                tenant_document.updated_date = datetime.now()
                tenant_document.save()
            transaction.savepoint_commit(sid)
            return tenant_document, True, error
        except Exception as e:
            print("Exception occured ", str(traceback.print_exc(e)))
            transaction.rollback(sid)
            error = str(traceback.print_exc(e))
            return tenant_document, False, error

# Save Tenant Sub modules
@transaction.atomic
def save_basic_tenant_sub_modules_details(request, user):
            sid = transaction.savepoint()
            tenant_sub_modules = ""
            error = ''
            try:
                tenant_sub_modules = tenant_sub_modules()
                if request.method == "POST":
                    if "subscription_id" in request.POST:
                        tenant_sub_modules.subscription_id = request.data["subscription_id"]
                    if "module_id" in request.POST:
                        tenant_sub_modules.module_id = request.data["module_id"]
                    if "sub_module_id" in request.POST:
                        tenant_sub_modules.sub_module_id = request.data["sub_module_id"]
                    if "sub_module_name" in request.POST:
                        tenant_sub_modules.sub_module_name = request.data["sub_module_name"]
                    if "is_active" in request.POST:
                        tenant_sub_modules.is_active = request.data["is_active"]

                    tenant_sub_modules.created_by = user.id
                    tenant_sub_modules.created_date = datetime.now()
                    tenant_sub_modules.save()
                if request.method == "PUT" and "tenant_id_string" in request.PUT:
                    tenant_sub_modules = tenant_sub_modules.objects.get(id_string=request.data["tenant_id_string"])
                    if "subscription_id" in request.POST:
                        tenant_sub_modules.subscription_id = request.data["subscription_id"]
                    if "module_id" in request.POST:
                        tenant_sub_modules.module_id = request.data["module_id"]
                    if "sub_module_id" in request.POST:
                        tenant_sub_modules.sub_module_id = request.data["sub_module_id"]
                    if "sub_module_name" in request.POST:
                        tenant_sub_modules.sub_module_name = request.data["sub_module_name"]
                    if "is_active" in request.POST:
                        tenant_sub_modules.is_active = request.data["is_active"]

                    tenant_sub_modules.updated_by = user.id
                    tenant_sub_modules.updated_date = datetime.now()
                    tenant_sub_modules.save()
                transaction.savepoint_commit(sid)
                return tenant_sub_modules, True, error
            except Exception as e:
                print("Exception occured ", str(traceback.print_exc(e)))
                transaction.rollback(sid)
                error = str(traceback.print_exc(e))
                return tenant_sub_modules, False, error

 # Save Tenant Payments aginast Invoices
@transaction.atomic
def save_basic_tenant_payments_details(request, user):
            sid = transaction.savepoint()
            tenant_basic_payments = ""
            error = ''
            try:
                tenant_basic_payments = tenant_basic_payments()
                if request.method == "POST":
                    if "invoice_number" in request.POST:
                        tenant_basic_payments.invoice_number = request.data["invoice_number"]
                    if "payment_method" in request.POST:
                        tenant_basic_payments.payment_method = request.data["payment_method"]
                        if "payment_channel" in request.POST:
                            tenant_basic_payments.payment_channel = request.data["payment_channel"]
                        if "transaction_no" in request.POST:
                            tenant_basic_payments.transaction_no = request.data["transaction_no"]
                        if "transaction_date" in request.POST:
                            tenant_basic_payments.transaction_date = request.data["transaction_date"]
                        if "amount" in request.POST:
                            tenant_basic_payments.amount = request.data["amount"]
                        if "tax_amount" in request.POST:
                            tenant_basic_payments.tax_amount = request.data["tax_amount"]
                        if "currency" in request.POST:
                            tenant_basic_payments.currency = request.data["currency"]
                        if "is_active" in request.POST:
                            tenant_basic_payments.is_active = request.data["is_active"]

                    tenant_basic_payments.created_by = user.id
                    tenant_basic_payments.created_date = datetime.now()
                    tenant_basic_payments.save()
                if request.method == "PUT" and "tenant_id_string" in request.PUT:
                    tenant_basic_payments = tenant_basic_payments.objects.get(id_string=request.data["tenant_id_string"])

                    if "invoice_number" in request.POST:
                        tenant_basic_payments.invoice_number = request.data["invoice_number"]
                    if "payment_method" in request.POST:
                        tenant_basic_payments.payment_method = request.data["payment_method"]
                    if "payment_channel" in request.POST:
                        tenant_basic_payments.payment_channel = request.data["payment_channel"]
                    if "transaction_no" in request.POST:
                        tenant_basic_payments.transaction_no = request.data["transaction_no"]
                    if "transaction_date" in request.POST:
                         tenant_basic_payments.transaction_date = request.data["transaction_date"]
                    if "amount" in request.POST:
                         tenant_basic_payments.amount = request.data["amount"]
                    if "tax_amount" in request.POST:
                         tenant_basic_payments.tax_amount = request.data["tax_amount"]
                    if "currency" in request.POST:
                        tenant_basic_payments.currency = request.data["currency"]
                    if "is_active" in request.POST:
                        tenant_basic_payments.is_active = request.data["is_active"]

                    tenant_basic_payments.updated_by = user.id
                    tenant_basic_payments.updated_date = datetime.now()
                    tenant_basic_payments.save()
                transaction.savepoint_commit(sid)
                return tenant_basic_payments, True, error
            except Exception as e:
                print("Exception occured ", str(traceback.print_exc(e)))
                transaction.rollback(sid)
                error = str(traceback.print_exc(e))
                return tenant_basic_payments, False, error


def save_payment_details(request, user, tenant):
    try:
        if request.data['payment_details'] == '':
            return True
        else:
            for payment_detail in request.data['payment_details']:
                service_type = get_service_type_by_id_string(payment_detail['service_type_id_string'])
                payment_type = get_payment_type_by_id_string(payment_detail['payment_type_id_string'])
                payment = Payment( # TODO: Payment  table is missing
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

def is_data_verified(request):  # todo - Black, Null, empty string - ready to use method by Django
        if request.data['name'] == '' and  \
                request.data['mobile_number'] == '' and request.data['email'] == '' and \
               request.data['is_vip'] == '' and request.data['address'] \
                and request.data['street'] == '' and request.data['zipcode'] == '' and \
                request.data['connectivity'] == '':
            return False
        else:
            return True

def is_subscription_data_verified(request):  # todo - Black, Null, empty string - ready to use method by Django
    if request.data['subscription_plan_id'] == '' and request.data['subscription_frequency_id'] == '':
        return False
    else:
        return True
def is_subscription_plan_data_verified(request):  # todo - Black, Null, empty string - ready to use method by Django
    if request.data['subscription_plan_id'] == '':
        return False
    else:
        return True

def is_submodule_data_verified(request):  # todo - Black, Null, empty string - ready to use method by Django
    if request.data['sub_module_name'] == '' :
        return False
    else:
        return True

def is_bank_data_verified(request):
    if request.data['bank']:
        return True
    else:
        return False


def set_validated_data(validated_data):
    if "area_id" in validated_data:
        area = get_area_by_id_string(validated_data["area_id"])
        validated_data["area_id"] = area.id
    if "status_id" in validated_data:
        tenant_status = get_tenant_status_by_id_string(validated_data["status_id"])
        validated_data["status_id"] = tenant_status.id
    if "country_id" in validated_data:
        country = get_country_by_id_string(validated_data["country_id"])
        validated_data["country_id"] = country.id
    if "state_id" in validated_data:
        state = get_state_by_id_string(validated_data["state_id"])
        validated_data["state_id"] = state.id
    if "city_id" in validated_data:
        city = get_city_by_id_string(validated_data["city_id"])
        validated_data["city_id"] = city.id

    return validated_data

def set_validated_data_submodule(validated_data):
    if "module_id" in validated_data:
        module = get_tenant_module_by_id_string(validated_data["module_id"])
        validated_data["module_id"] = module.id

    return validated_data

def set_validated_data_subscription_plan(validated_data):
    if "subscription_plan_id" in validated_data:
        subscription_plan = get_subscription_plan_by_id_string(validated_data["subscription_plan_id"])
        validated_data["subscription_plan_id"] = subscription_plan.id
    return validated_data