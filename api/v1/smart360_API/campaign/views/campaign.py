import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.smart360_API.campaign.views.common_functions import is_token_valid, get_payload, \
    get_filtered_campaign, check_authorization, get_user

from api.v1.smart360_API.lookup.models.privillege import Privillege
from api.v1.smart360_API.lookup.models.sub_module import SubModule
from api.v1.smart360_API.smart360_API.settings import DISPLAY_DATE_FORMAT



# Api for getting campaign list, filter, search
class CampaignListApiView(APIView):

    def get(self, request, format=None):
        try:
            campaign_list = []

            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])

                # Checking authorization start
                privillege = Privillege.objects.filter(id = 1)
                sub_module = SubModule.objects.filter(id = 1)
                if check_authorization(user, privillege, sub_module):

                     # Code for filtering campaign start
                    campaigns = get_filtered_campaign(user, request)

                    # Code for sending campaigns in response
                    for campaign in campaigns:
                        campaign_list.append({
                            'cam_group' : campaign.cam_group,
                            'name' : campaign.name,
                            'status' : Status.objects.get(id = campaign.status_id).status,
                            'description' : campaign.description,
                            'budget_amount' : campaign.budget_amount,
                            'actual_amount' : campaign.actual_amount,
                            'area' : Area.objects.get(id = campaign.area_id).area,
                            'sub_area' : SubArea.objects.get(id = campaign.sub_area_id).sub_area,
                            'category': Category.objects.get(id=campaign.category_id).category,
                            'sub_category': SubCategory.objects.get(id=campaign.sub_category_id).sub_category,
                            'created_on' : campaign.created_date.strftime(DISPLAY_DATE_FORMAT)
                        })
                    return Response({
                        'success': 'true',
                        'data': campaign_list,
                        'message': 'Data sent successfully.'
                    }, status=status.HTTP_200_OK)

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


