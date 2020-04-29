from django.db.models import Q
from django.core.paginator import Paginator
from v1.registration.models.survey import Survey, get_registration_by_id_string
from v1.registration.models.survey_consumer import SurveyConsumer
from django.db import transaction
from api.settings import DISPLAY_DATE_FORMAT

from v1.commonapp.models.Survey import get_survey_by_id_string
from v1.commonapp.models.survey_consumer import get_survey_consumer_by_id_string
from v1.commonapp.models.survey_status import get_survey_status_by_id_string,get_survey_status_by_id
from v1.commonapp.models.survey_type import get_survey_type_by_id_string,get_survey_type_by_id
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string





def get_filtered_location_survey(request, user):
    total_pages = ''
    page_no = ''
    surveys = Survey.objects.filter(tenant_id=user.tenant_id,
                                                utility_id__in=user.data_access.all())
    if request.data['utillity']:
        surveys = surveys.objects.filter(utility_id= request.data['utillity'])

    if request.data['category']:
        surveys = surveys.objects.filter(category=request.data['category'])

    if request.data['sub_category']:
        surveys = surveys.objects.filter(sub_category=request.data['sub_category'])

    if request.data['objective']:
        surveys = surveys.objects.filter(objective= request.data['objective'])

    if request.data['area']:
        surveys = surveys.objects.filter(area= request.data['area'])

    if request.data['sub_area']:
        surveys = surveys.objects.filter(sub_area= request.data['subarea'])

    if request.data['status']:
        surveys = surveys.objects.filter(status= request.data['status'])

    if request.data['search_text'] == '':
        pass
    else:
        surveys = surveys.filter(
            Q(name__icontains=request.data['search_text']) |
            Q(area__icontains=request.data['search_text']))

    if request.data['page_number'] == '':
        paginator = Paginator(surveys,int(request.data['page_size']))
        total_pages = str(paginator.num_pages)
        page_no = '1'
        surveys = paginator.page(1)
        return surveys,total_pages,page_no
    else:
        paginator = Paginator(surveys, int(request.data['page_size']))
        total_pages = str(paginator.num_pages)
        page_no = request.data['page_number']
        surveys = paginator.page(int(page_no))

        return surveys, total_pages, page_no


def get_filtered_consumer_survey(request,user):
    total_pages = ''
    page_no = ''
    surveys = SurveyConsumer.objects.filter(tenant_id=user.tenant_id,
                                    utility_id__in=user.data_access.all(),survey_id=request.data['survey_id'])
    if request.data['utillity']:
        surveys = surveys.objects.filter(utility_id=request.data['utillity'])

    if request.data['category']:
        surveys = surveys.objects.filter(category=request.data['category'])

    if request.data['sub_category']:
        surveys = surveys.objects.filter(sub_category=request.data['sub_category'])

    if request.data['objective']:
        surveys = surveys.objects.filter(objective=request.data['objective'])

    if request.data['area']:
        surveys = surveys.objects.filter(area=request.data['area'])

    if request.data['sub_area']:
        surveys = surveys.objects.filter(sub_area=request.data['subarea'])

    if request.data['status']:
        surveys = surveys.objects.filter(status=request.data['status'])

    if request.data['search_text'] == '':
        pass
    else:
        surveys = surveys.filter(
            Q(name__icontains=request.data['search_text']) |
            Q(consumer_no__icontains=request.data['search_text']))

    if request.data['page_number'] == '':
        paginator = Paginator(surveys, int(request.data['page_size']))
        total_pages = str(paginator.num_pages)
        page_no = '1'
        surveys = paginator.page(1)
        return surveys, total_pages, page_no
    else:
        paginator = Paginator(surveys, int(request.data['page_size']))
        total_pages = str(paginator.num_pages)
        page_no = request.data['page_number']
        surveys = paginator.page(int(page_no))

        return surveys, total_pages, page_no

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
        consumer_id = get_survey_consumer_by_id_string(request.data['consumer_id_string'])
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
            consumer_survey = SurveyConsumer(
                tenant=user.tenant,
                utility=utility,
                survey_id=consumer_survey.id,
                consumer_no=request.data['consumer_no'],
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
            consumer_survey = get_survey_consumer_by_id_string(request.data['consumer_id_string'])
            consumer_survey.tenant = user.tenant
            consumer_survey.utility = utility
            consumer_survey.survey_id = consumer_survey.id
            consumer_survey.status_id = status.id
            consumer_survey.is_active = True            
            consumer_survey.save()
            transaction.savepoint_commit(sid)
            return consumer_survey
    except Exception as e:
        transaction.rollback(sid)
        consumer_survey = ''
        return consumer_survey
