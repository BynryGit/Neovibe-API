import traceback
from django.db.models import Q
from rest_framework import status
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from datetime import datetime
from django.core.paginator import Paginator
from v1.survey.models.survey import Survey
from v1.survey.models.survey_consumer import SurveyConsumer
from django.db import transaction
from v1.consumer.models.consumer_category import get_consumer_category_by_id,get_consumer_category_by_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.supplier.models.supplier import get_supplier_by_id_string
from v1.survey.models.survey import get_survey_by_id_string
from v1.survey.models.survey_consumer import get_survey_consumer_by_id_string
from v1.survey.models.survey_status import get_survey_status_by_id_string,get_survey_status_by_id
from v1.survey.models.survey_type import get_survey_type_by_id_string,get_survey_type_by_id
from v1.survey.models.survey_assignment import SurveyAssignment
from v1.survey.models.survey_objective import get_survey_objective_by_id_string,get_survey_objective_by_id
from v1.commonapp.models.area import get_area_by_id_string,get_area_by_id
from v1.commonapp.models.sub_area import get_sub_area_by_id
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.survey.models.survey_type import get_survey_type_by_id_string
from v1.survey.models.survey_subtype import get_survey_subtype_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.views.logger import logger





def get_filtered_location_survey(user,request):
    total_pages = ''
    page_no = ''
    survey = ''
    error = ''
    try:
        survey = Survey.objects.filter(tenant=user.tenant)

        if "utility" in request.data:
            survey = survey.objects.filter(utility=request.data['utility'])

        if "category" in request.data:
            survey = survey.objects.filter(category_id=request.data['category'])

        if "sub_category" in request.data:
            survey = survey.objects.filter(sub_category_id=request.data['sub_category'])

        if "status" in request.data:
            survey = survey.objects.filter(status_id=request.data['status'])

        if "type" in request.data:
            survey = survey.objects.filter(type_id=request.data['type'])

        if "area" in request.data:
            survey = survey.objects.filter(area_id=request.data['area'])

        if "subarea" in request.data:
            survey = survey.objects.filter(sub_area_id=request.data['subarea'])

        if "objective" in request.data:
            survey = survey.objects.filter(objective_id=request.data['objective'])

        if "search_text" in request.data:
            if request.data['search_text'] == '':
                pass
            else:
                survey = survey.filter(
                    Q(name__icontains=request.data['search_text']) |
                    Q(no_of_consumers__icontains=request.data['search_text']))

        if "page_number" in request.data:
            if request.data['page_number'] == '':
                paginator = Paginator(survey, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = '1'
                survey = paginator.page(1)
            else:
                paginator = Paginator(survey, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = request.data['page_number']
                survey = paginator.page(int(page_no))
        return survey, total_pages, page_no, True, error
    except Exception as e:
        print("Exception occured ",str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return survey, total_pages, page_no, False, error


def get_filtered_consumer_survey(user,request):
    total_pages = ''
    page_no = ''
    survey_consumer = ''
    error = ''
    try:
        # if 'survey_id' in request.headers:
        #     survey_consumer = SurveyConsumer.objects.filter(tenant=user.tenant,survey_id=request.data['survey_id'])
        # else:
        survey_consumer = SurveyConsumer.objects.filter(tenant=user.tenant)

        if "utility" in request.data:
            survey_consumer = survey_consumer.objects.filter(utility=request.data['utility'])

        if "category" in request.data:
            survey_consumer = survey_consumer.objects.filter(category_id=request.data['category'])

        if "sub_category" in request.data:
            survey_consumer = survey_consumer.objects.filter(sub_category_id=request.data['sub_category'])

        if "area" in request.data:
            survey_consumer = survey_consumer.objects.filter(area_id=request.data['area'])

        if "subarea" in request.data:
            survey_consumer = survey_consumer.objects.filter(sub_area_id=request.data['subarea'])

        if "survey_id" in request.data:
            survey_consumer = survey_consumer.objects.filter(survey_id=request.data['survey_id'])

        if "vendor_id" in request.data:
            survey_consumer = survey_consumer.objects.filter(vendor_id=request.data['vendor_id'])
        if "search_text" in request.data:
            if request.data['search_text'] == '':
                pass
            else:
                survey_consumer = survey_consumer.filter(
                    Q(name__icontains=request.data['search_text']) |
                    Q(consumer_no__icontains=request.data['search_text']))

        if "page_number" in request.data:
            if request.data['page_number'] == '':
                paginator = Paginator(survey_consumer, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = '1'
                survey_consumer = paginator.page(1)
            else:
                paginator = Paginator(survey_consumer, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = request.data['page_number']
                survey_consumer = paginator.page(int(page_no))
        return survey_consumer, total_pages, page_no, True, error
    except Exception as e:
        print("Exception occured ", str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return survey_consumer, total_pages, page_no, False, error


def is_data_verified(request):
    return True
    if request.data['survey_name'] == "" and request.data['survey_type'] == "" and request.data['start_date'] == "" and \
       request.data['end_date'] == "" and request.data['discription'] == "" and request.data['objective'] == "" \
       and request.data['category'] == "" and request.data['sub_category'] == "" and request.data['area'] == "" and request.data['sub_area'] == "":
        return False
    else:
        return True

def save_survey_details(user,request,sid):
    survey= ''
    try:
        survey = Survey()
        if "survey_name" in request.data:
            survey.name = request.data['survey_name']
        if "objective_id_string" in request.data:
            objective = get_survey_objective_by_id_string(request.data['objective_id_string'])
            survey.objective_id = objective.id
        if "description" in request.data:
            survey.description = request.data['description']
        if "type_id_string" in request.data:
            type = get_survey_type_by_id_string(request.data['type_id_string'])
            survey.type_id = type.id
        if "category_id_string" in request.data:
            consumer_category = get_consumer_category_by_id_string(request.data['category_id_string'])
            survey.category_id = consumer_category.id
        if "sub_category_id_string" in request.data:
            sub_category = get_consumer_sub_category_by_id_string(request.data['sub_category_id_string'])
            survey.sub_category_id = sub_category.id
        if "area_id_string" in request.data:
            area = get_area_by_id_string(request.data['area_id_string'])
            survey.area_id = area.id
        if "sub_area_id_string" in request.data:
            sub_area = get_sub_area_by_id_string(request.data['sub_area_id_string'])
            survey.sub_area_id = sub_area.id
        if "status_id_string" in request.data:
            status = get_survey_status_by_id_string(request.data['status_id_string'])
            survey.status_id = status.id
        if "no_of_consumers" in request.data:
            survey.no_of_consumers = request.data['no_of_consumers']
        if "start_date" in request.data:
            survey.start_date = request.data['start_date']
        if "end_date" in request.data:
            survey.end_date = request.data['end_date']
        if "completion_date" in request.data:
            survey.completion_date = request.data['completion_date']

        survey.tenant = user.tenant
        survey.created_by = user.id
        survey.created_date = datetime.now()
        survey.save()
        return survey, True
    except Exception as e:
        print("Exception occured ", str(traceback.print_exc(e)))
        transaction.rollback(sid)
        return survey, False

def save_edit_location_survey_details(user,request):
    survey = ''
    try:
        if "survey_id_string" in request.data:
            survey = get_survey_by_id_string(request.data['survey_id_string'])
        if "survey_name" in request.data:
            survey.name = request.data['survey_name']
        if "objective_id_string" in request.data:
            objective = get_survey_objective_by_id_string(request.data['objective_id_string'])
            survey.objective_id = objective.id
        if "description" in request.data:
            survey.description = request.data['description']
        if "type_id_string" in request.data:
            type = get_survey_type_by_id_string(request.data['type_id_string'])
            survey.type_id = type.id
        if "category_id_string" in request.data:
            consumer_category = get_consumer_category_by_id_string(request.data['category_id_string'])
            survey.category_id = consumer_category.id
        if "sub_category_id_string" in request.data:
            sub_category = get_consumer_sub_category_by_id_string(request.data['sub_category_id_string'])
            survey.sub_category_id = sub_category.id
        if "area_id_string" in request.data:
            area = get_area_by_id_string(request.data['area_id_string'])
            survey.area_id = area.id
        if "sub_area_id_string" in request.data:
            sub_area = get_sub_area_by_id_string(request.data['sub_area_id_string'])
            survey.sub_area_id = sub_area.id
        if "status_id_string" in request.data:
            status = get_survey_status_by_id_string(request.data['status_id_string'])
            survey.status_id = status.id
        if "no_of_consumers" in request.data:
            survey.no_of_consumers = request.data['no_of_consumers']
        if "start_date" in request.data:
            survey.start_date = request.data['start_date']
        if "end_date" in request.data:
            survey.end_date = request.data['end_date']
        if "completion_date" in request.data:
            survey.completion_date = request.data['completion_date']

        survey.tenant = user.tenant
        survey.updated_by = user.id
        survey.updated_date = datetime.now()
        survey.save()
        return survey, True
    except Exception as e:
        print("Exception occured ", str(traceback.print_exc(e)))
        transaction.rollback(sid)
        return survey, False



def get_consumer_survey_list():
    try:
        consumer_obj = SurveyConsumer.objects.filter(survey_id=1)
        consumer_list = []

        for consumer in consumer_obj:
            consumer_data = {}
            # Code for lookups start
            area = get_area_by_id(consumer.area_id)
            sub_area = get_sub_area_by_id(consumer.sub_area_id)
            # Code for lookups end

            consumer_data['tenant_id_string'] = consumer.tenant.id_string
            consumer_data['utility_id_string']= consumer.utility.id_string
            consumer_data['first_name']= consumer.first_name
            consumer_data['last_name']= consumer.last_name
            consumer_data['consumer_no']= consumer.consumer_no
            consumer_data['survey_id']= consumer.survey_id
            consumer_data['area_id_string']= area.id_string
            consumer_data['sub_area_id_string']= sub_area.id_string
            consumer_list.append(consumer_data)
        return consumer_list
    except Exception as e:
        pass

def is_consumer_data_verified(request):
    return True
    if request.data['survey_name'] == "" and request.data['survey_type'] == "" and request.data['start_date'] == "" and \
       request.data['end_date'] == "" and request.data['discription'] == "" and request.data['objective'] == "" and request.data['utility'] == ""\
       and request.data['category'] == "" and request.data['area'] == "" and request.data['sub_area'] == "" \
       and request.data['consumer_no'] == "" and request.data['no_of_consumers'] == "":
        return False
    else:
        return True


def save_consumer_survey_details(user,request,sid):
    try:

        utility = UtilityMaster.objects.get(id_string=request.data['utility'])  # Don't have table
        area = get_area_by_id_string(request.data['area'])
        sub_area = get_sub_area_by_id_string(request.data['sub_area'])
        type = get_survey_type_by_id_string(request.data['type'])
        objective = get_survey_type_by_id_string(request.data['objective'])
        status = get_survey_status_by_id_string(request.data['status'])

        if request.data['consumer_id_string'] == "":
            consumer_survey = Survey(
                tenant=user.tenant,
                utility=utility,
                name=request.data['survey_name'],
                start_date=request.data['start_date'],
                end_date=request.data['end_date'],
                description=request.data['description'],
                objective=objective.id,
                no_of_consumers=request.data['no_of_consumers'],
                completion_date=request.data['completion_date'],
                type=type.id,
                area=area.id,
                sub_area=sub_area.id,
                status_id=status.id,
                is_active=True
            )
            consumer_survey.save()
            transaction.savepoint_commit(sid)
            return consumer_survey
        else:
            consumer_survey = get_survey_by_id_string(request.data['consumer_id_string'])
            consumer_survey.tenant = user.tenant
            consumer_survey.utility = utility
            consumer_survey.consumer_no = request.data['consumer_no']
            consumer_survey.name = request.data['survey_name']
            consumer_survey.start_date = request.data['start_date']
            consumer_survey.end_date = request.data['end_date']
            consumer_survey.description = request.data['description']
            consumer_survey.objective = objective.id
            consumer_survey.no_of_consumers = request.data['no_of_consumers'],
            consumer_survey.completion_date = request.data['completion_date'],
            consumer_survey.type = type.id
            consumer_survey.area = area.id
            consumer_survey.sub_area = sub_area.id
            consumer_survey.status_id = status.id
            consumer_survey.save()
            transaction.savepoint_commit(sid)
            return consumer_survey
    except Exception as e:
        transaction.rollback(sid)
        consumer_survey = ''
        return consumer_survey

def save_consumer_details(request, user,consumer_survey):
    consumer_data_list = []
    try:

        # Sample data of Consumers
        consumer_datas = [{'first_name': 'priyanka','last_name':'kachare','email_id':'priya@gmail.com', 'phone_mobile': '9011613929',
                       'area_id_string': "42531c10-5c0b-439d-879a-31c5e2dd5c85", 'sub_area_id_string':"1c3f6828-f09c-48eb-9bb7-2661b4f48fe7",'consumer_no':554811464894,
                           'category_id_id_string': "2f2433db-db13-409d-a297-3819c919417a", 'sub_category_id_id_string':"8e3c0605-8ad9-4e0f-a6fb-29011ec57384"},
                        {'first_name': 'ravi', 'last_name':'patil','email_id':'ravi@gmail.com','phone_mobile': '7620983335',
                       'area_id_string': "42531c10-5c0b-439d-879a-31c5e2dd5c85", 'sub_area_id_string': "1c3f6828-f09c-48eb-9bb7-2661b4f48fe7",'consumer_no':895455546544,
                         'category_id_string': "2f2433db-db13-409d-a297-3819c919417a", 'sub_category_id_string':"8e3c0605-8ad9-4e0f-a6fb-29011ec57384"}]

        for consumer_data in consumer_datas:
            surveyconsumer = SurveyConsumer()
            if 'first_name' in consumer_data:
                surveyconsumer.first_name = consumer_data['first_name']
            if 'last_name' in consumer_data:
                surveyconsumer.last_name = consumer_data['last_name']
            if 'email_id' in consumer_data:
                surveyconsumer.email_id = consumer_data['email_id']
            if 'phone_mobile' in consumer_data:
                surveyconsumer.phone_mobile = consumer_data['phone_mobile']
            if 'consumer_no' in consumer_data:
                surveyconsumer.consumer_no = consumer_data['consumer_no']
            if 'area_id_string' in consumer_data:
                area = get_area_by_id_string(consumer_data["area_id_string"])
                surveyconsumer.area_id = area.id
            if "sub_area_id_string" in consumer_data:
                sub_area = get_sub_area_by_id_string(consumer_data["sub_area_id_string"])
                surveyconsumer.sub_area_id = sub_area.id
            if "category_id_string" in consumer_data:
                consumer_category = get_consumer_category_by_id_string(consumer_data["category_id_string"])
                surveyconsumer.category_id = consumer_category.id
            if "sub_category_id_string" in consumer_data:
                sub_category = get_consumer_sub_category_by_id_string(consumer_data["sub_category_id_string"])
                surveyconsumer.sub_category_id = sub_category.id


            surveyconsumer.tenant = user.tenant
            surveyconsumer.survey_id = consumer_survey.id
            surveyconsumer.vendor_id = 1
            surveyconsumer.created_by = user.id
            surveyconsumer.created_date = datetime.now()
            surveyconsumer.save()
            consumer_data_list.append(surveyconsumer)
        return consumer_data_list,True
    except Exception as e:
        print("Exception occured ", str(traceback.print_exc(e)))
        return consumer_data_list, False

def save_edit_consumer_details(user,request):
    surveyconsumer = ''
    try:
        if "consumer_id_string" in request.data:
            surveyconsumer = get_survey_consumer_by_id_string(request.data['consumer_id_string'])
        if 'first_name' in request.data:
            surveyconsumer.first_name = request.data['first_name']
        if 'last_name' in request.data:
            surveyconsumer.last_name = request.data['last_name']
        if 'email_id' in request.data:
            surveyconsumer.email_id = request.data['email_id']
        if 'phone_mobile' in request.data:
            surveyconsumer.phone_mobile = request.data['phone_mobile']
        if 'consumer_no' in request.data:
            surveyconsumer.consumer_no = request.data['consumer_no']
        if 'area_id_string' in request.data:
            area = get_area_by_id_string(request.data["area_id_string"])
            surveyconsumer.area_id = area.id
        if "sub_area_id_string" in request.data:
            sub_area = get_sub_area_by_id_string(request.data["sub_area_id_string"])
            surveyconsumer.sub_area_id = sub_area.id
        if "category_id_string" in request.data:
            consumer_category = get_consumer_category_by_id_string(request.data["category_id_string"])
            surveyconsumer.category_id = consumer_category.id
        if "sub_category_id_string" in request.data:
            sub_category = get_consumer_sub_category_by_id_string(request.data["sub_category_id_string"])
            surveyconsumer.sub_category_id = sub_category.id
        surveyconsumer.updated_by = user.id
        surveyconsumer.updated_date = datetime.now()
        surveyconsumer.save()
        return surveyconsumer,True
    except Exception as e:
        print("Exception occured ", str(traceback.print_exc(e)))
        return surveyconsumer, False


def is_assignment_verified(request):
    if request.data['vendor_id_string'] == "" and request.data['survey_id_string'] == "" and request.data['assigned_date'] =="" \
       and request.data['completion_date'] == "":
        return False
    else:
        return True

@transaction.atomic
def save_vendor_assignment_details(request,user):
    sid = transaction.savepoint()
    try:
        utility = UtilityMaster.objects.get(id_string=request.data['utility'])  # Don't have table
        vendor_details = VendorDetails.objects.get(id_string=request.data['vendor_id_string'])
        survey_details = get_survey_by_id_string(request.data['survey_id_string'])
        status = get_survey_status_by_id(survey_details.status)
        survey_assignment = SurveyAssignment(
            tenant=user.tenant,
            utility=utility,
            survey_id=survey_details.id,
            vendor_id=vendor_details.id,
            assigned_date=request.data['assigned_date'],
            completion_date=request.data['completion_date'],
            status_id=status.id,
            is_active=True
        )
        survey_assignment.save()
        transaction.savepoint_commit(sid)
        return survey_assignment
    except Exception as e:
        transaction.rollback(sid)
        survey_assignment = ''
        return survey_assignment
        pass

def set_survey_validate_data(validated_data):
    if "objective_id" in validated_data:
        objective_id = get_survey_objective_by_id_string(validated_data['objective_id'])
        validated_data["objective_id"] = objective_id.id

    if "type_id" in validated_data:
        type_id = get_survey_type_by_id_string(validated_data["type_id"])
        validated_data["type_id"] = type_id.id

    if "status_id" in validated_data:
        status_id = get_survey_status_by_id_string(validated_data["status_id"])
        validated_data["status_id"] = status_id.id

    if "category_id" in validated_data:
        consumer_category = get_consumer_category_by_id_string(validated_data["category_id"])
        validated_data["category_id"] = consumer_category.id

    if "sub_category_id" in validated_data:
        sub_category = get_consumer_sub_category_by_id_string(validated_data["sub_category_id"])
        validated_data["sub_category_id"] = sub_category.id

    if "area_id" in validated_data:
        area = get_area_by_id_string(validated_data["area_id"])
        validated_data["area_id"] = area.id

    if "sub_area_id" in validated_data:
        sub_area = get_sub_area_by_id_string(validated_data["sub_area_id"])
        validated_data["sub_area_id"] = sub_area.id

    if "vendor_id" in validated_data:
        vendor_id = get_supplier_by_id_string(validated_data["vendor_id"])
        validated_data["vendor_id"] = vendor_id.id

    if "survey_id" in validated_data:
        survey_id = get_survey_by_id_string(validated_data["survey_id"])
        validated_data["survey_id"] = survey_id.id

    return validated_data


def set_survey_type_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data

def set_survey_subtype_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "survey_type_id" in validated_data:
        survey_type = get_survey_type_by_id_string(validated_data["survey_type_id"])
        if survey_type:
            validated_data["survey_type_id"] = survey_type.id
        else:
            raise CustomAPIException("Survey Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    
    return validated_data


def set_survey_objective_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "survey_type_id" in validated_data:
        survey_type = get_survey_type_by_id_string(validated_data["survey_type_id"])
        if survey_type:
            validated_data["survey_type_id"] = survey_type.id
        else:
            raise CustomAPIException("Survey Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    
    if "survey_subtype_id" in validated_data:
        survey_subtype = get_survey_subtype_by_id_string(validated_data["survey_subtype_id"])
        if survey_subtype:
            validated_data["survey_subtype_id"] = survey_subtype.id
        else:
            raise CustomAPIException("Survey Sub Type not found.", status_code=status.HTTP_404_NOT_FOUND)
    
    return validated_data

