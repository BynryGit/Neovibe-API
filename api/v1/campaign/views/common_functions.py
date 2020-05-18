import traceback
from datetime import datetime
from v1.campaign.models.campaign import Campaign
from v1.campaign.models.advertisement import Advertisements
from v1.campaign.models.advert_status import get_advert_status_by_id_string
from v1.consumer.models.consumer_category import get_consumer_category_by_id,get_consumer_category_by_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.campaign.models.advertisement import get_advertisements_by_id_string
from django.core.paginator import Paginator
from django.db import transaction
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.commonapp.models.frequency import get_frequency_by_id_string
from v1.campaign.models.campaign import get_campaign_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string



# getting list data
def get_filtered_campaign(user,request):
    total_pages = ''
    page_no = ''
    campaigns = ''
    error = ''
    try:
        campaign = Campaign.objects.filter(tenant=user.tenant)

        if "utility" in request.data:
            campaign = campaign.objects.filter(utility=request.data['utility'])

        if "group" in request.data:
            campaign = campaign.objects.filter(group_id=request.data['group'])

        if "objective" in request.data:
            campaign = campaign.objects.filter(objective_id=request.data['objective'])

        if "frequency" in request.data:
            campaign = campaign.objects.filter(frequency_id=request.data['frequency'])

        if "category" in request.data:
            campaign = campaign.objects.filter(category_id=request.data['category'])

        if "sub_category" in request.data:
            campaign = campaign.objects.filter(sub_category_id=request.data['sub_category'])

        if "status" in request.data:
            campaign = campaign.objects.filter(status_id=request.data['status'])

        if "search_text" in request.data:
            if request.data['search_text'] == '':
                pass
            else:
                campaign = campaign.objects.filter(name__icontains=request.data['search_text'])

        if "page_number" in request.data:
            if request.data['page_number'] == '':
                paginator = Paginator(campaign,int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = '1'
                campaigns = paginator.page(1)
            else:
                paginator = Paginator(campaign, int(request.data['page_size']))
                total_pages = str(paginator.num_pages)
                page_no = request.data['page_number']
                campaigns = paginator.page(int(page_no))
        return campaign,total_pages, page_no, True, error
    except Exception as e:
        print("Exception occured ",str(traceback.print_exc(e)))
        error = str(traceback.print_exc(e))
        return campaigns, total_pages, page_no, False, error


# verify the advertisement data
def is_advertisement_verified(request):
    return True
    if request.data['advertisements_name'] == '' and request.data['budget_amount'] == '' and request.data['actual_amount'] == ''and \
        request.data['area'] == '' and request.data['sub_area'] == '' and request.data['start_date'] == '' and request.data['end_date'] == '' and \
        request.data['description'] == ''and request.data['campaign_id_string'] == '' and request.data['frequency_id_string'] == '':
        return False
    else:
        return True


# save the campign details start
@transaction.atomic
def save_campaign_details(request, user,sid):
    campaign = ""
    try:
        campaign = Campaign()
        if "campaign_name" in request.data:
            campaign.name = request.data['campaign_name']
        if "start_date" in request.data:
            campaign.start_date = request.data['start_date']
        if "end_date" in request.data:
            campaign.end_date = request.data['end_date']
        if "description" in request.data:
            campaign.description = request.data['description']
        if "potential_consumers" in request.data:
            campaign.potential_consumers = request.data['potential_consumers']
        if "actual_consumers" in request.data:
            campaign.actual_consumers = request.data['actual_consumers']
        if "budget_amount" in request.data:
            campaign.budget_amount = request.data['budget_amount']
        if "actual_amount" in request.data:
            campaign.actual_amount = request.data['actual_amount']
        if "utility_id_string" in request.data:
            utility = get_utility_by_id_string(request.data["utility_id_string"])
            campaign.utility_id = utility.id
        if "frequency_id_string" in request.data:
            frequency = get_frequency_by_id_string(request.data['frequency_id_string'])
            campaign.frequency_id = frequency.id
        if "category_id_string" in request.data:
            consumer_category = get_consumer_category_by_id_string(request.data["category_id_string"])
            campaign.category_id = consumer_category.id
        if "sub_category_id_string" in request.data:
            sub_category = get_consumer_sub_category_by_id_string(request.data["sub_category_id_string"])
            campaign.sub_category_id = sub_category.id
        if "area_id_string" in request.data:
            area = get_area_by_id_string(request.data["area_id_string"])
            campaign.area_id = area.id
        if "sub_area_id_string" in request.data:
            sub_area = get_sub_area_by_id_string(request.data["sub_area_id_string"])
            campaign.sub_area_id = sub_area.id

        campaign.tenant = user.tenant
        campaign.created_by = user.id
        campaign.created_date = datetime.now()
        campaign.save()
        return campaign, True
    except Exception as e:
        print("Exception occured ", str(traceback.print_exc(e)))
        transaction.rollback(sid)
        return campaign, False

# save the campign details end


# save advertisement details start
@transaction.atomic
def save_advertisement_details(user,campaign,sid):
    advertise_list = []
    try:
        # Sample data of Advertisement
        advertises = [{'advertisements_name':'Smart360-Awareness-Power','area':'shivaji nagar','sub_area':'l1',
                       'start_date':'2020-01-22','end_date':'2020-03-21','budget_amount':3000,'actual_amount':6000,
                        'description':'This campaign for Awareness of Power','campaign_id_string':'31950b44-6f5a-4551-9058-95f4bdddb08f',
                        'frequency_id_string':'1874cf50-c3d7-478f-b6c3-5814062f1873',"utility_id_string":"20f7fd7f-0750-4531-8a54-2a8a172c678c",
                       "area_id_string":"1c2da9b5-eb4b-4c47-b1dd-84e085d9d1b7",
                        "sub_area_id_string":"4c96a5ee-03f9-49d3-8dbf-559b4cdc756e",},
                      {'advertisements_name': 'Smart360-Awareness-Gas', 'area': 'Kothrud', 'sub_area': 'bhusari colony',
                       'start_date': '2020-01-01', 'end_date': '2020-03-30','budget_amount':4000,'actual_amount':7000,
                        'description':'This campaign for Awareness of Gas','campaign_id_string':'31950b44-6f5a-4551-9058-95f4bdddb08f',
                        'frequency_id_string':'8b563e69-5250-494f-8900-f92e59b8388d',"utility_id_string":"aaa573b6-bde1-44af-921a-cf0a5a49a4a9",
                       "area_id_string":"1c2da9b5-eb4b-4c47-b1dd-84e085d9d1b7",
                        "sub_area_id_string":"4c96a5ee-03f9-49d3-8dbf-559b4cdc756e",}]

        for advertise in advertises:
            advertisement = Advertisements()
            if "advertisements_name" in advertise:
                advertisement.name = advertise['advertisements_name']
            if "area_id_string" in advertise:
                area = get_area_by_id_string(advertise["area_id_string"])
                advertisement.area_id = area.id
            if "sub_area_id_string" in advertise:
                sub_area = get_sub_area_by_id_string(advertise["sub_area_id_string"])
                advertisement.sub_area_id = sub_area.id
            if "start_date" in advertise:
                advertisement.start_date = advertise['start_date']
            if "end_date" in advertise:
                advertisement.end_date = advertise['end_date']
            if "description" in advertise:
                advertisement.description = advertise['description']

            if "utility_id_string" in advertise:
                utility = get_utility_by_id_string(advertise["utility_id_string"])
                advertisement.utility_id = utility.id
            if "campaign_id_string" in advertise:
                advertisement.campaign_id = campaign.id
            if "budget_amount" in advertise:
                advertisement.budget_amount = advertise['budget_amount']
            if "actual_amount" in advertise:
                advertisement.actual_amount = advertise['actual_amount']
            if "frequency_id_string" in advertise:
                frequency = get_frequency_by_id_string(advertise['frequency_id_string'])
                advertisement.frequency_id = frequency.id

            advertisement.tenant = user.tenant
            advertisement.created_by = user.id
            advertisement.created_date = datetime.now()
            advertisement.save()
            advertise_list.append(advertisement)
        return True,advertise_list
    except Exception as e:
        print("Exception occured ", str(traceback.print_exc(e)))
        transaction.rollback(sid)
        return advertise_list, False

# save advertisement details end


def save_edited_basic_campaign_details(request, user):
    campaign = ''
    try:
        if "campaign_id_string" in request.data:
            campaign = get_campaign_by_id_string(request.data["campaign_id_string"])
        if "campaign_name" in request.data:
            campaign.name = request.data['campaign_name']
        if "start_date" in request.data:
            campaign.start_date = request.data['start_date']
        if "end_date" in request.data:
            campaign.end_date = request.data['end_date']
        if "description" in request.data:
            campaign.description = request.data['description']
        if "potential_consumers" in request.data:
            campaign.potential_consumers = request.data['potential_consumers']
        if "actual_consumers" in request.data:
            campaign.actual_consumers = request.data['actual_consumers']
        if "budget_amount" in request.data:
            campaign.budget_amount = request.data['budget_amount']
        if "actual_amount" in request.data:
            campaign.actual_amount = request.data['actual_amount']
        if "utility_id_string" in request.data:
            utility = get_utility_by_id_string(request.data["utility_id_string"])
            campaign.utility_id = utility.id
        if "frequency_id_string" in request.data:
            frequency = get_frequency_by_id_string(request.data['frequency_id_string'])
            campaign.frequency_id = frequency.id
        if "category_id_string" in request.data:
            consumer_category = get_consumer_category_by_id_string(request.data["category_id_string"])
            campaign.category_id = consumer_category.id
        if "sub_category_id_string" in request.data:
            sub_category = get_consumer_sub_category_by_id_string(request.data["sub_category_id_string"])
            campaign.sub_category_id = sub_category.id
        if "area_id_string" in request.data:
            area = get_area_by_id_string(request.data["area_id_string"])
            campaign.area_id = area.id
        if "sub_area_id_string" in request.data:
            sub_area = get_sub_area_by_id_string(request.data["sub_area_id_string"])
            campaign.sub_area_id = sub_area.id
        campaign.updated_by = user.id
        campaign.updated_date = datetime.now()
        campaign.save()
        return campaign, True
    except Exception as e:
        print("Exception occured ", str(traceback.print_exc(e)))
        return campaign, False

def save_edited_basic_advertisement_details(request, user):
    advertisement = ''
    campaign = ''
    try:
        if "advert_id_string" in request.data:
            advertisement = get_advertisements_by_id_string(request.data['advert_id_string'])
            if "campaign_id_string" in request.data:
                campaign = get_campaign_by_id_string(request.data["campaign_id_string"])
            if "advertisements_name" in request.data:
                advertisement.name = request.data['advertisements_name']
            if "area_id_string" in request.data:
                area = get_area_by_id_string(request.data["area_id_string"])
                advertisement.area_id = area.id
            if "sub_area_id_string" in request.data:
                sub_area = get_sub_area_by_id_string(request.data["sub_area_id_string"])
                advertisement.sub_area_id = sub_area.id
            if "start_date" in request.data:
                advertisement.start_date = request.data['start_date']
            if "end_date" in request.data:
                advertisement.end_date = request.data['end_date']
            if "description" in request.data:
                advertisement.description = request.data['description']
            if "utility_id_string" in request.data:
                utility = get_utility_by_id_string(request.data["utility_id_string"])
                advertisement.utility_id = utility.id
            if "campaign_id_string" in request.data:
                advertisement.campaign_id = campaign.id
            if "budget_amount" in request.data:
                advertisement.budget_amount = request.data['budget_amount']
            if "actual_amount" in request.data:
                advertisement.actual_amount = request.data['actual_amount']
            if "frequency_id_string" in request.data:
                frequency = get_frequency_by_id_string(request.data['frequency_id_string'])
                advertisement.frequency_id = frequency.id

            advertisement.updated_by = user.id
            advertisement.updated_date = datetime.now()
            advertisement.save()
            return advertisement, True
    except Exception as e:
        print("Exception occured ", str(traceback.print_exc(e)))
        return advertisement, False



from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.country import get_country_by_id_string
from v1.commonapp.models.state import get_state_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string
from v1.consumer.models.consumer_ownership import get_consumer_ownership_by_id_string
from v1.consumer.models.consumer_scheme_master import get_scheme_by_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.consumer.models.source_type import get_source_type_by_id_string
from v1.payment.models.consumer_payment import get_payment_by_id_string
from v1.registration.models.registration_status import get_registration_status_by_id_string
from v1.registration.models.registration_type import get_registration_type_by_id_string


def is_data_verified(request):
    return True


def set_validated_data(validated_data):

    if "frequency_id" in validated_data:
        frequency = get_frequency_by_id_string(validated_data['frequency_id'])
        validated_data["frequency_id"] = frequency.id
    if "consumer_category_id" in validated_data:
        consumer_category = get_consumer_category_by_id_string(validated_data["consumer_category_id"])
        validated_data["consumer_category_id"] = consumer_category.id
    if "sub_category_id" in validated_data:
        sub_category = get_consumer_sub_category_by_id_string(validated_data["sub_category_id"])
        validated_data["sub_category_id"] = sub_category.id
    if "area_id" in validated_data:
        area = get_area_by_id_string(validated_data["area_id"])
        validated_data["area_id"] = area.id
    if "sub_area_id" in validated_data:
        sub_area = get_sub_area_by_id_string(validated_data["sub_area_id"])
        validated_data["sub_area_id"] = sub_area.id

    return validated_data





















