from api.v1.smart360_API.smart360_API.campaign.models.campaign_master import Campaign
from api.v1.smart360_API.smart360_API.campaign.models.advertisements import Advertisements

from api.v1.smart360_API.lookup.models.area import get_area_by_id_string
from api.v1.smart360_API.commonapp.models.sub_area import get_sub_area_by_id_string
from api.v1.smart360_API.commonapp.models.frequency import get_frequency_by_id_string





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
        request.data['description'] == ''and request.data['campaign_id_string'] == '' and request.data['frequency_id_string'] == '' and\
        request.data['objective_id_string'] == '':
        return False
    else:
        return True


def save_advertisement_details(request,id_string):
    campaign_obj = Campaign.objects.get(id_string=id_string)
    utility = UtilityMaster.objects.get(id_string=request.data['utility'])  # Don't have table
    area = get_area_by_id_string(request.data['area'])
    sub_area = get_sub_area_by_id_string(request.data['sub_area'])
    frequency = get_frequency_by_id_string(request.data['frequency'])

    # Sample data of Advertisement
    advertises = [{'advertisements_name':'Smart360-Awareness-Power','area':'shivaji nagar','sub_area':'l1',
                   'start_date':'21 jan 2020','end_date':'21 mar 2020','budget_amount':3000,'actual_amount':6000,
                    'description':'This campaign for Awareness of Power','campaign_id_string':'hsvjnc',
                    'frequency_id_string':'fttdfwgdgskh','objective_id_string':'vydhfdigf'},
                  {'advertisements_name': 'Smart360-Awareness-Gas', 'area': 'Kothrud', 'sub_area': 'bhusari colony',
                   'start_date': '1 jan 2020', 'end_date': '30 mar 2020','budget_amount':4000,'actual_amount':7000,
                    'description':'This campaign for Awareness of Gas','campaign_id_string':'uheui',
                    'frequency_id_string':'fbdhkfbk','objective_id_string':'bfjedvfj'}]

    for advertise in advertises:
         advertise_obj = Advertisements(
             name = advertise['advertisements_name'],
             area = area.id,
             sub_area = sub_area.id,
             start_date = advertise['start_date'],
             end_date = advertise['end_date'],
             description = advertise['description'],
             campaign_id = campaign_obj.id,
             budget_amount = advertise['budget_amount'],
             actual_amount = advertise['actual_amount'],
             frequency_id = frequency.id,

         )
         advertise_obj.save()

     return advertise_obj



