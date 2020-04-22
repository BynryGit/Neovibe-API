import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.smart360_API.registration.views.common_functions import is_token_valid, get_payload, \
     check_authorization, get_user

from api.v1.smart360_API.smart360_API.messages import STATE,SUCCESS,ERROR,EXCEPTION
from api.v1.smart360_API.lookup.models.privillege import Privillege
from api.v1.smart360_API.lookup.models.sub_module import SubModule
from api.v1.smart360_API.campaign.models.campaign_master import CampaignMaster


# API Header
# API end Point: api/v1/campaign
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Campaign
# Interaction: Add Campaign
# Usage: API for Add Campaign
# Tables used: 2.3.6 Campaign Master
# Auther: Priyanka
# Created on: 22/04/2020


# Api for add campaign details
class AddCampaignApi(APIView):

    def post(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])

                # Checking authorization start
                privillege = Privillege.objects.filter(id = 1)
                sub_module = SubModule.objects.filter(id = 1)
                if check_authorization(user, privillege, sub_module):

                    # Code for add campaign start
                    # first check values are present or not
                    if request.data['campaign_name'] and request.data['campaign_type'] and request.data['area'] and\
                          request.data['sub_area'] and request.data['start_date'] and request.data['end_date']:

                        # check Campaign is Already Exists or not
                        if CampaignMaster.objects.get(area=request.data['area'],sub_area=request.data['sub_area'],
                                                      start_date=request.data['start_date'],end_date=request.data['end_date']):

                            campaign_data = {'campaign_name':request.data['campaign_name'],'area':request.data['area'],
                                             'sub_area':request.data['sub_area'],'start_date':request.data['start_date'],'end_date':request.data['end_date']}

                            return Response({
                                STATE: ERROR,
                                'data': campaign_data,
                            }, status=status.HTTP_409_CONFLICT)
                        else:
                            # save campaign details
                            campaignmaster = CampaignMaster(
                                tenant=TenantMaster.objects.get(id=request.data['tenant_id']), #TODO:  Wrapper
                                utility=UtilityMaster.objects.get(id=request.data['utility']), #TODO: Change to utility_id
                                name=request.data['campaign_name'],
                                cam_group_id=request.data['cam_gr_id_string'],
                                category_id=request.data['category_id_string'], #TODO: Write function to get category by IDstring.
                                sub_category_id=request.data['sub_cat_id_string'],
                                start_date=request.data['start_date'],
                                end_date=request.data['end_date'],
                                portion_id=request.data['portion_id_string'], #TODO:  to be removed
                                mru_id=request.data['mru_id_string'], #TODO:  to be removed
                                doc_url=request.data['document_url'], ##TODO:  use global method
                                description=request.data['description'], #TODO: limit to be added. txt -250, desc -1000
                            )
                            campaignmaster.save()

                            return Response({
                                STATE: SUCCESS,
                                'data':'', 
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
                    }, status=status.HTTP_401_UNAUTHORIZED)
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


