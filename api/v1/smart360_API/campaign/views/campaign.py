import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.smart360_API.campaign.views.common_functions import is_token_valid, get_payload, \
     check_authorization, get_user,get_filtered_campaign

from api.v1.smart360_API.lookup.models.privilege import get_privilege_by_id
from api.v1.smart360_API.lookup.models.sub_module import get_sub_module_by_id
from api.v1.smart360_API.commonapp.common_functions import get_payload,get_user,is_authorized,is_token_valid
from api.v1.smart360_API.smart360_API.messages import STATE,SUCCESS,ERROR,EXCEPTION
from api.v1.smart360_API.lookup.models.privilege import Privilege
from api.v1.smart360_API.lookup.models.sub_module import SubModule
from api.v1.smart360_API.campaign.models.campaign import Campaign

# API Header
# API end Point: api/v1/campaign/list
# API verb: GET
# Package: Basic
# Modules: S&M
# Sub Module: Campaign
# Interaction: List Campaign
# Usage: API will fetch required data for Campaign list
# Tables used: 2.3.6 Campaign Master
# Auther: Priyanka Kachare
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

                    # Code for sending campaigns in response
                    for campaign in campaigns:
                        campaign_list.append({
                            'cam_type': CampaignType.objects.get(id_string=campaign.type_id).campaign_type,
                            'status' : Status.objects.get(id_string = campaign.status_id).status_name,
                            'category': Category.objects.get(id_string=campaign.category_id).category_name,
                            'sub_category': SubCategory.objects.get(id_string=campaign.sub_category_id).sub_category_name,
                            'frequency':Frequency.objects.get(id_string=campaign.frequency_id).frequency_name,
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
# Auther: Priyanka Kachare
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


                    # Code for add campaign start
                    # first check values are present or not
                    if request.data['campaign_name'] and request.data['campaign_type'] and request.data['area'] and\
                       request.data['sub_area'] and request.data['start_date'] and request.data['end_date'] and request.data['description'] and\
                       request.data['cam_gr_id_string'] and request.data['category_id_string'] and request.data['sub_cat_id_string']:

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
                                tenant=TenantMaster.objects.get(id=request.data['tenant_id']), #TODO:  Wrapper
                                utility=UtilityMaster.objects.get(id=request.data['utility_id']),
                                name=request.data['campaign_name'],
                                cam_type_id=CampaignType.objects.get(id_string=request.data['cam_type_id_string']).campaign_type,
                                start_date=request.data['start_date'],
                                end_date=request.data['end_date'],
                                description=request.data['description'],
                                frequency_id=Frequency.objects.get(id_string=request.data['frequency_id']).frequency_name,
                                category_id=Category.objects.get(id_string=request.data['category_id_string']).category_name,
                                sub_category_id=SubCategory.objects.get(id_string=request.data['sub_cat_id_string']).sub_category_name,
                                area=areas.objects.get(id_string=request.data['area_id_string']).area_name,
                                sub_area=sub_areas.objects.get(id_string=request.data['subarea_id_string']).sub_area_name,
                                status_id=Status.objects.get(id_string = request.data['status_id']).status_name,
                            )
                            campaign_details.save()

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
# API verb: POST
# Package: Basic
# Modules: S&M
# Sub Module: Campaign
# Interaction: Add Campaign
# Usage: API for Add Campaign
# Tables used: 2.3.6 Campaign Master
# Auther: Priyanka Kachare
# Created on: 22/04/2020