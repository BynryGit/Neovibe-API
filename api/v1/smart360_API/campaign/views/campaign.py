import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.smart360_API.registration.views.common_functions import is_token_valid, get_payload, \
     check_authorization, get_user

from api.v1.smart360_API.lookup.models.privillege import Privillege
from api.v1.smart360_API.lookup.models.sub_module import SubModule
from api.v1.smart360_API.campaign.models.campaign_master import CampaignMaster


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
                                'success': 'false',
                                'data': campaign_data,
                                'message': 'Campaign Already Exists.'
                            }, status=status.HTTP_409_CONFLICT)
                        else:

                            campaignmaster = CampaignMaster(
                                tenant=TenantMaster.objects.get(id=request.data['tenant_id']),
                                utility=UtilityMaster.objects.get(id=request.data['utility']),
                                name=request.data['campaign_name'],
                                cam_group_id=request.data['cam_gr_id_string'],
                                category_id=request.data['category_id_string'],
                                sub_category_id=request.data['sub_cat_id_string'],
                                start_date=request.data['start_date'],
                                end_date=request.data['end_date'],
                                doc_url=request.data['document_url'],
                                description=request.data['description'],
                            )
                            campaignmaster.save()

                            return Response({
                                'success': 'true',
                                'data': '',
                                'message': 'Data Save Successfully.'
                            }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            'success': 'false',
                            'data': '',
                            'message': 'Some values are missing'
                        }, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({
                        'success': 'false',
                        'data': '',
                        'message': 'User does not have required privillege.',
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    'success': 'false',
                    'data': '',
                    'message': 'Please login first.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'success': 'false',
                'error': str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


