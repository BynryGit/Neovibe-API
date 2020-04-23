from api.v1.smart360_API.smart360_API.campaign.models.campaign_master import Campaign
from api.v1.smart360_API.smart360_API.campaign.models.advertisements import Advertisements

from api.v1.smart360_API.lookup.models.area import get_area_by_id_string
from api.v1.smart360_API.lookup.models.sub_area import get_sub_area_by_id_string
from api.v1.smart360_API.lookup.models.frequency import get_frequency_by_id_string
from api.v1.smart360_API.lookup.models.camp_type import get_camp_type_by_id_string
from api.v1.smart360_API.lookup.models.consumer_category import get_consumer_category_by_id_string
from api.v1.smart360_API.lookup.models.area import get_area_by_id_string
from api.v1.smart360_API.lookup.models.sub_area import get_sub_area_by_id_string







def get_filtered_campaign(request, user):
    campaign = Campaign.objects.filter(tenant_id=user.tenant_id,
                                                utility_id__in=user.data_access.all())

    if request.data['cam_type_id']:
        campaign = campaign.objects.filter(type_id=request.data['cam_type_id'])

    if request.data['frequency_id']:
        campaign = campaign.objects.filter(frequency_id=request.data['frequency_id'])

    if request.data['category_id']:
        campaign = campaign.objects.filter(category_id=request.data['category_id'])

    if request.data['sub_category_id']:
        campaign = campaign.objects.filter(sub_category_id=request.data['sub_category_id'])

    if request.data['status_id']:
        campaign = campaign.objects.filter(status_id=request.data['status_id'])

    return campaign


def is_data_verified(request):
    if request.data['campaign_name'] == '' and request.data['campaign_type'] == '' and request.data['area'] == ''and \
        request.data['sub_area'] == '' and request.data['start_date'] == '' and request.data['end_date'] == '' and \
        request.data['description'] == ''and request.data['cam_gr_id_string'] == '' and \
        request.data['category_id_string'] == '' and request.data['sub_cat_id_string'] == '':
        return False
    else:
        return True


def is_advertisement_verified(request):
    if request.data['advertisements_name'] == '' and request.data['budget_amount'] == '' and request.data['actual_amount'] == ''and \
        request.data['area'] == '' and request.data['sub_area'] == '' and request.data['start_date'] == '' and request.data['end_date'] == '' and \
        request.data['description'] == ''and request.data['campaign_id_string'] == '' and request.data['frequency_id_string'] == '':
        return False
    else:
        return True


def save_advertisement_details(request,user,id_string):
    try:
        campaign_obj = Campaign.objects.get(id_string=id_string)
        utility = UtilityMaster.objects.get(id_string=request.data['utility'])  # Don't have table
        area = get_area_by_id_string(request.data['area'])
        sub_area = get_sub_area_by_id_string(request.data['sub_area'])
        frequency = get_frequency_by_id_string(request.data['frequency'])

        # Sample data of Advertisement
        advertises = [{'advertisements_name':'Smart360-Awareness-Power','area':'shivaji nagar','sub_area':'l1',
                       'start_date':'21 jan 2020','end_date':'21 mar 2020','budget_amount':3000,'actual_amount':6000,
                        'description':'This campaign for Awareness of Power','campaign_id_string':'hsvjnc',
                        'frequency_id_string':'fttdfwgdgskh'},
                      {'advertisements_name': 'Smart360-Awareness-Gas', 'area': 'Kothrud', 'sub_area': 'bhusari colony',
                       'start_date': '1 jan 2020', 'end_date': '30 mar 2020','budget_amount':4000,'actual_amount':7000,
                        'description':'This campaign for Awareness of Gas','campaign_id_string':'uheui',
                        'frequency_id_string':'fbdhkfbk'}]

        for advertise in advertises:
             advertise_obj = Advertisements(
                 tenant=user.tenant,
                 utility=utility,
                 name = advertise['advertisements_name'],
                 area = area.id,
                 sub_area = sub_area.id,
                 start_date = advertise['start_date'],
                 end_date = advertise['end_date'],
                 description = advertise['description'],
                 campaign_id = campaign_obj.id,
                 budget_amount = advertise['budget_amount'],
                 actual_amount = advertise['actual_amount'],
                 frequency_id = frequency.id
             )
             advertise_obj.save()
        return advertise_obj
    except Exception as e:
        return e


def get_campaign_details(user, request,camp_id_string):
    try:
        campaign_obj = Campaign.objects.get(id_string=camp_id_string)
        frequency_obj = get_frequency_by_id_string(campaign_obj.frequency_id)
        camp_type_obj = get_camp_type_by_id_string(campaign_obj.type_id)
        category_obj = get_consumer_category_by_id_string(campaign_obj.category_id)
        area = get_area_by_id_string(campaign_obj.area_id)
        sub_area = get_sub_area_by_id_string(campaign_obj.sub_area_id)
        campaign_details = {
            'camp_id':campaign_obj.id,
            'camp_name':campaign_obj.name,
            'frequency':frequency_obj.frequency,
            'utility':campaign_obj.utility.name,
            'type':camp_type_obj.campaign_type,
            'category':category_obj.category_name,
            'area':area.area_name,
            'sub_area':sub_area.sub_area_name,
            'start_date':campaign_obj.start_date,
            'end_date':campaign_obj.end_date,
            'description':campaign_obj.description if campaign_obj.description else '',
        }
        advertisements = Advertisements.objects.filter(campaign_id = camp_id_string)
        advertisement_list = []
        if advertisements:
            for advertisement in advertisements:
                advertisement_details = {
                    'advertisement_name':advertisement.name,
                    'description':advertisement.description,
                    'actual_amount':advertisement.actual_amount,
                    'start_date':advertisement.start_date,
                    'end_date':advertisement.end_date,
                    'area':area.area_name,
                    'sub_area':sub_area.sub_area_name,
                    'category':category_obj.category_name,
                    'frequency':frequency_obj.frequency_name,
                    }
                advertisement_list.append(advertisement_details)

        return campaign_details,advertisement_list

    except Exception as e:
        return e



