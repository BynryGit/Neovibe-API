import traceback
from django.db.models import Q
from django.core.paginator import Paginator
from v1.survey.models.survey import Survey
from v1.survey.models.survey_consumer import SurveyConsumer
from django.db import transaction
from api.settings import DISPLAY_DATE_FORMAT

from v1.survey.models.survey import get_survey_by_id_string
from v1.survey.models.survey_consumer import get_survey_consumer_by_id_string
from v1.survey.models.survey_status import get_survey_status_by_id_string,get_survey_status_by_id
from v1.survey.models.survey_type import get_survey_type_by_id_string,get_survey_type_by_id
from v1.survey.models.survey_assignment import SurveyAssignment
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string





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


def is_data_verified(request, user):
    if request.data['survey_name'] == "" and request.data['survey_type'] == "" and request.data['start_date'] == "" and \
       request.data['end_date'] == "" and request.data['discription'] == "" and request.data['objective'] == "" and request.data['utility'] == ""\
       and request.data['category'] == "" and request.data['area'] == "" and request.data['sub_area'] == "":
        return False
    else:
        return True

@transaction.atomic
def save_location_survey_details(request, user):
    sid = transaction.savepoint()
    try:
        utility = UtilityMaster.objects.get(id_string=request.data['utility'])  # Don't have table
        area = get_area_by_id_string(request.data['area'])
        sub_area = get_sub_area_by_id_string(request.data['sub_area'])
        type = get_survey_type_by_id_string(request.data['type'])
        objective = get_survey_type_by_id_string(request.data['objective'])
        status = get_survey_status_by_id_string(request.data['status'])

        if request.data['survey_id_string'] == "":
            location_survey = Survey(
                tenant=user.tenant,
                utility=utility,
                name=request.data['survey_name'],
                start_date=request.data['start_date'],
                end_date=request.data['end_date'],
                description=request.data['description'],
                objective = objective.id,
                completion_date = request.data['completion_date'],
                type = type.id,
                area=area.id,
                sub_area=sub_area.id,
                status_id=status.id,
                is_active = True
            )
            location_survey.save()
            transaction.savepoint_commit(sid)
            return location_survey
        else:
            location_survey = get_survey_by_id_string(request.data['survey_id_string'])
            location_survey.tenant = user.tenant
            location_survey.utility = utility
            location_survey.name = request.data['survey_name']
            location_survey.start_date = request.data['start_date']
            location_survey.end_date = request.data['end_date']
            location_survey.description = request.data['description']
            location_survey.objective = objective.id
            location_survey.completion_date = request.data['completion_date'],
            location_survey.type = type.id
            location_survey.area = area.id
            location_survey.sub_area = sub_area.id
            location_survey.status_id = status.id
            location_survey.save()
            transaction.savepoint_commit(sid)
            return location_survey
    except Exception as e:
        transaction.rollback(sid)
        location_survey = ''
        return location_survey


def get_consumer_survey_list(request,user):
    try:
        consumer_obj = SurveyConsumer.objects.filter(survey_id=request.data['survey_id'])
        consumer_list = []
        for consumer in consumer_obj:
            consumer_data = {}
            # Code for lookups start
            area = get_area_by_id_string(consumer.id_string)
            sub_area = get_sub_area_by_id_string(consumer.id_string)
            type = get_survey_type_by_id_string(consumer.id_string)
            objective = get_survey_type_by_id_string(consumer.id_string)
            status = get_survey_status_by_id_string(consumer.id_string)
            # Code for lookups end

            consumer_data['tenant_id_string']: consumer.tenant.id_string
            consumer_data['utility_id_string']: consumer.utility.id_string
            consumer_data['name']: consumer.name
            consumer_data['objective']: objective.id_string
            consumer_data['discription']: consumer.description
            consumer_data['type']: type.id_string
            consumer_data['no_of_consumers']: consumer.no_of_consumers
            consumer_data['start_date']: consumer.start_date.strftime(DISPLAY_DATE_FORMAT)
            consumer_data['end_date']: consumer.end_date.strftime(DISPLAY_DATE_FORMAT)
            consumer_data['completion_date']: consumer.completion_date.strftime(DISPLAY_DATE_FORMAT)
            consumer_data['area_id_string']: area.id_string
            consumer_data['sub_area_id_string']: sub_area.id_string
            consumer_data['status']: status.id_string
            consumer_list.append(consumer_data)

        return consumer_list

    except Exception as e:
        pass

def is_consumer_data_verified(request,user):
    if request.data['survey_name'] == "" and request.data['survey_type'] == "" and request.data['start_date'] == "" and \
       request.data['end_date'] == "" and request.data['discription'] == "" and request.data['objective'] == "" and request.data['utility'] == ""\
       and request.data['category'] == "" and request.data['area'] == "" and request.data['sub_area'] == "" \
       and request.data['consumer_no'] == "" and request.data['no_of_consumers'] == "":
        return False
    else:
        return True


@transaction.atomic
def save_consumer_survey_details(request,user):
    sid = transaction.savepoint()
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

@transaction.atomic
def save_consumer_details(request, user,consumer_survey):
    sid = transaction.savepoint()
    try:
        utility = UtilityMaster.objects.get(id_string=request.data['utility'])  # Don't have table
        survey_id = get_survey_by_id_string(request.data['id_string'])
        status = get_survey_status_by_id_string(request.data['status'])

        if request.data['consumer_id_string'] == "":
            # Sample data of Consumers
            consumer_datas = [{'consumer_name': 'priyanka', 'mobile_no': '9011613929', 'meter_no': '859756547895',
                           'area': 'Kothrud', 'sub_area': 'bhusari colony','consumer_no':554811464894,
                           'description': 'This updated information'},
                            {'consumer_name': 'ravi', 'mobile_no': '7620983335', 'meter_no': '2568756547895',
                           'area': 'nagar', 'sub_area': 'bhusari colony','consumer_no':895455546544,
                           'description': 'This updated information'}]

            consumer_data_list = []
            for consumer_data in consumer_datas:
                consumer_survey = SurveyConsumer(
                    tenant=user.tenant,
                    utility=utility,
                    survey_id=survey_id.id,
                    consumer_no=consumer_data['consumer_no'],
                    consumer_name=consumer_data['consumer_name'],
                    mobile_no=consumer_data['mobile_no'],
                    meter_no=consumer_data['meter_no'],
                    area=consumer_data['area'],
                    sub_area=consumer_data['sub_area'],
                    description=consumer_data['description'],
                    status_id=status.id,
                    is_active=True
                )
                consumer_survey.save()
                transaction.savepoint_commit(sid)
                consumer_data_list.append(consumer_survey)
            return consumer_data_list
        else:
            consumer_survey = get_survey_consumer_by_id_string(request.data['consumer_id_string'])
            consumer_survey.tenant = user.tenant
            consumer_survey.utility = utility
            consumer_survey.survey_id = consumer_survey.id
            consumer_survey.consumer_no = consumer_survey.consumer_no,
            consumer_survey.consumer_name = consumer_survey.consumer_name,
            consumer_survey.mobile_no = consumer_survey.mobile_no,
            consumer_survey.meter_no = consumer_survey.meter_no,
            consumer_survey.area = consumer_survey.area,
            consumer_survey.sub_area = consumer_survey.sub_area,
            consumer_survey.description = consumer_survey.description,
            consumer_survey.status_id = status.id
            consumer_survey.is_active = True
            consumer_survey.save()
            transaction.savepoint_commit(sid)
            return consumer_survey

    except Exception as e:
        transaction.rollback(sid)
        consumer_data_list = ''
        return consumer_data_list


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



