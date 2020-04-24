from api.v1.smart360_API.smart360_API.campaign.models.campaign_master import Campaign
from api.v1.smart360_API.smart360_API.campaign.models.advertisements import Advertisements
from api.v1.smart360_API.campaign.models.campaign_status import get_cam_status_by_tenant_id_string
from api.v1.smart360_API.commonapp.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from api.v1.smart360_API.lookup.models.camp_type import get_camp_type_by_id_string
from api.v1.smart360_API.lookup.models.consumer_category import get_consumer_category_by_id_string
from api.v1.smart360_API.lookup.models.area import get_area_by_id_string

from api.v1.smart360_API.commonapp.models.sub_area import get_sub_area_by_id_string
from api.v1.smart360_API.commonapp.models.frequency import get_frequency_by_id_string
from api.v1.smart360_API.commonapp.models.campaign import get_campaign_by_id_string



# getting list data
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


# verify the campaign data
def is_data_verified(request):
    if request.data['campaign_name'] == '' and request.data['campaign_type'] == '' and request.data['area'] == ''and \
        request.data['sub_area'] == '' and request.data['start_date'] == '' and request.data['end_date'] == '' and \
        request.data['description'] == ''and request.data['cam_gr_id_string'] == '' and \
        request.data['category_id_string'] == '' and request.data['sub_cat_id_string'] == '':
        return False
    else:
        return True

# verify the advertisement data
def is_advertisement_verified(request):
    if request.data['advertisements_name'] == '' and request.data['budget_amount'] == '' and request.data['actual_amount'] == ''and \
        request.data['area'] == '' and request.data['sub_area'] == '' and request.data['start_date'] == '' and request.data['end_date'] == '' and \
        request.data['description'] == ''and request.data['campaign_id_string'] == '' and request.data['frequency_id_string'] == '':
        return False
    else:
        return True


# save the campign details start
def save_campaign_details(request, user):
    try:
        # Code for lookups start
        utility = UtilityMaster.objects.get(id_string=request.data['utility'])  # Don't have table
        status = get_cam_status_by_tenant_id_string(request.data['camp_status'])
        campaigns_type = get_camp_type_by_id_string(request.data['campaigns_type'])
        category = get_consumer_category_by_id_string(request.data['consumer_category'])
        sub_category = get_consumer_sub_category_by_id_string(request.data['consumer_sub_category'])
        frequency = get_frequency_by_id_string(request.data['frequency'])
        area = get_area_by_id_string(request.data['area'])
        sub_area = get_sub_area_by_id_string(request.data['sub_area'])
        # Code for lookups end

        if request.data['camp_id_string'] == '':
            campaign_details = Campaign(
                tenant=user.tenant,
                utility=utility,
                name=request.data['campaign_name'],
                cam_type_id=campaigns_type.id,
                start_date=request.data['start_date'],
                end_date=request.data['end_date'],
                description=request.data['description'],
                frequency_id=frequency.id,
                category_id=category.id,
                sub_category_id=sub_category.id,
                area=area.id,
                sub_area=sub_area.id,
                status_id=status.id
            )
            campaign_details.save()
            return campaign_details
        else:
            campaign_details = get_campaign_by_id_string(request.data['camp_id_string'])
            campaign_details.tenant = user.tenant,
            campaign_details.utility = utility,
            campaign_details.name = request.data['campaign_name'],
            campaign_details.cam_type_id = campaigns_type.id,
            campaign_details.start_date = request.data['start_date'],
            campaign_details.end_date = request.data['end_date'],
            campaign_details.description = request.data['description'],
            campaign_details.frequency_id = frequency.id,
            campaign_details.category_id = category.id,
            campaign_details.sub_category_id = sub_category.id,
            campaign_details.area = area.id,
            campaign_details.sub_area = sub_area.id,
            campaign_details.status_id = status.id
            campaign_details.save()
            return campaign_details
    except Exception as e:
        return e
    # save the campign details end


# save advertisement details start
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
        advertise_list = []
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
                 campaign_id = campaign_obj.id_string,
                 budget_amount = advertise['budget_amount'],
                 actual_amount = advertise['actual_amount'],
                 frequency_id = frequency.id
             )
             advertise_obj.save()
             advertise_list.append(advertise_obj)
        return advertise_list
    except Exception as e:
        return e
# save advertisement details end






















