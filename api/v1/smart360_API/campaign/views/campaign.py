import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.smart360_API.campaign.views.common_functions import is_token_valid, get_payload, \
     check_authorization, get_user,get_filtered_campaign,is_data_verified,is_advertisement_verified,\
    save_advertisement_details,get_campaign_details

from api.v1.smart360_API.lookup.models.privilege import get_privilege_by_id
from api.v1.smart360_API.lookup.models.sub_module import get_sub_module_by_id
from api.v1.smart360_API.commonapp.models.consumer_category import get_consumer_category_by_id_string,get_category_by_tenant_id_string
from api.v1.smart360_API.commonapp.models.consumer_sub_category import get_consumer_sub_category_by_id_string,get_sub_category_by_tenant_id_string
from api.v1.smart360_API.commonapp.models.frequency import get_frequency_by_tenant_id_string,get_frequency_by_id_string
from api.v1.smart360_API.lookup.models.camp_type import get_camp_type_by_tenant_id_string,get_camp_type_by_id_string
from api.v1.smart360_API.campaign.models.campaign_status import get_cam_status_by_tenant_id_string
from api.v1.smart360_API.lookup.models.area import get_area_by_id_string
from api.v1.smart360_API.commonapp.models.sub_area import get_sub_area_by_id_string

from api.v1.smart360_API.commonapp.common_functions import get_payload,get_user,is_authorized,is_token_valid
from api.v1.smart360_API.smart360_API.messages import STATE,SUCCESS,ERROR,EXCEPTION
from api.v1.smart360_API.campaign.models.campaign import Campaign

# API Header
# API end Point: api/v1/campaign/list
# API verb: GET
# Package: Basic
# Modules: S&M
# Sub Module: Campaign
# Interaction: Campaign List
# Usage: API will fetch required data for Campaign list
# Tables used: 2.3.6 Campaign Master
# Auther: Priyanka
# Created on: 22/04/2020

# Api for getting campaign  filter
class CampaignListApiView(APIView):

    def get(self, request, format=None):
        try:
            campaign_list = []

            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])

                # Checking authorization start
                privilege = get_privilege_by_id(1)
                sub_module = get_sub_module_by_id(1)
                if is_authorized(user, privilege, sub_module):
                # Checking authorization end

                    # Code for filtering campaign start
                    campaigns = get_filtered_campaign(user, request)
                    # Code for filtering campaign end

                    # Code for lookups start
                    statuses = Status.objects.all()
                    campaigns_type = get_camp_type_by_tenant_id_string(user.tenant.id_string)
                    category = get_category_by_tenant_id_string(user.tenant.id_string)
                    sub_category = get_sub_category_by_tenant_id_string(user.tenant.id_string)
                    frequency = get_frequency_by_tenant_id_string(user.tenant.id_string)
                    # Code for lookups end

                    # Code for sending campaigns in response
                    for campaign in campaigns:
                        campaign_list.append({
                            'cam_type': campaigns_type.objects.get(id_string = campaign.type_id).campaign_type,
                            'category': category.objects.get(id_string = campaign.category_id).category_name,
                            'sub_category': sub_category.objects.get(id_string = campaign.sub_category_id).sub_category_name,
                            'frequency':frequency.objects.get(id_string = campaign.frequency_id).frequency_name,
                            'status': statuses.objects.get(id_string = campaign.status_id).status_name,
                        })
                    return Response({
                         STATE: SUCCESS,
                         'data':campaign_list,
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({
                        STATE: ERROR,
                        'data':'',
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                    'data':'',
                }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# API Header
# API end Point: api/v1/campaign
# API verb: POST
# Package: Basic
# Modules: S&M
# Sub Module: Campaign
# Interaction: Add Campaign
# Usage: API for Add Campaign
# Tables used: 2.3.6 Campaign Master
# Auther: Priyanka
# Created on: 22/04/2020


# API for add campaign details
class AddCampaignApi(APIView):

    def post(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
            # Checking authentication end

                # Checking authorization start
                privilege = get_privilege_by_id(1)
                sub_module = get_sub_module_by_id(1)
                if is_authorized(user, privilege, sub_module):
                # Checking authorization end

                    # Code for lookups start
                    status = get_cam_status_by_tenant_id_string(request.data['camp_status'])
                    campaigns_type = get_camp_type_by_id_string(request.data['campaigns_type'])
                    category = get_consumer_category_by_id_string(request.data['consumer_category'])
                    sub_category = get_consumer_sub_category_by_id_string(request.data['consumer_sub_category'])
                    frequency = get_frequency_by_id_string(request.data['frequency'])
                    area = get_area_by_id_string(request.data['area'])
                    sub_area = get_sub_area_by_id_string(request.data['sub_area'])
                    # Code for lookups end

                    # Code for add campaign start

                    # Request data verification start
                    if is_data_verified(request, user):
                    # Request data verification end

                        # check Campaign is Already Exists or not
                        if Campaign.objects.get(area=request.data['area'],sub_area=request.data['sub_area'],
                                                start_date=request.data['start_date'],end_date=request.data['end_date']):

                            campaign_data = {'campaign_name':request.data['campaign_name'],'area':request.data['area'],
                                             'sub_area':request.data['sub_area'],'start_date':request.data['start_date'],'end_date':request.data['end_date']}

                            return Response({
                                STATE: ERROR,
                                'data': campaign_data,
                            }, status=status.HTTP_409_CONFLICT)
                        else:
                            # save campaign details
                            campaign_details = Campaign(
                                tenant=TenantMaster.objects.get(id_string=request.data['tenant_id_string']), #TODO:  Wrapper
                                utility=UtilityMaster.objects.get(id_string=request.data['utility_id_str']),
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

                            # Request advertisement verification start
                            if is_advertisement_verified(request,user):
                            # Request advertisement verification end

                                # save advertisement details start
                                save_advertisement_details(request,user,campaign_details.id_string)
                                # save advertisement details end

                            return Response({
                                STATE: SUCCESS,
                                'data':campaign_details,
                            }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                             STATE: ERROR,
                             'data': '',
                        }, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({
                        STATE: ERROR,
                        'data': '',
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                    'data': '',
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API Header
# API end Point: api/v1/campaign
# API verb: GET
# Package: Basic
# Modules: S&M
# Sub Module: Campaign
# Interaction: View Campaign Details
# Usage: API for Add View Campaign Details
# Tables used: 2.3.6 Campaign Master
# Auther: Priyanka
# Created on: 22/04/2020


# Api for getting campaign  details
class CampaignDetailsApiView(APIView):

    def get(self, request, format=None):
        try:
            campaign_list = []

            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
            # Checking authentication end

                # Checking authorization start
                privilege = get_privilege_by_id(1)
                sub_module = get_sub_module_by_id(1)
                if is_authorized(user, privilege, sub_module):
                # Checking authorization end

                    # Code for getting campaign  details start
                    camp_id_string = request.data['camp_id_string']
                    get_campaign_details(user, request,camp_id_string)
                    # Code for getting campaign  details end


                else:
                    return Response({
                        STATE: ERROR,
                        'data': '',
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                    'data': '',
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





