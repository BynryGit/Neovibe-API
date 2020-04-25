import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.v1.smart360_API.smart360_API.settings import DISPLAY_DATE_FORMAT

from api.v1.smart360_API.campaign.views.common_functions import is_token_valid, get_payload, \
     check_authorization, get_user,get_filtered_campaign,is_data_verified,is_advertisement_verified,\
    save_advertisement_details,save_campaign_details
from api.v1.smart360_API.smart360_API.campaign.models.advertisements import Advertisements
from api.v1.smart360_API.smart360_API.campaign.models.advert_status import get_cam_status_by_tenant_id_string

from api.v1.smart360_API.lookup.models.privilege import get_privilege_by_id
from api.v1.smart360_API.lookup.models.sub_module import get_sub_module_by_id
from api.v1.smart360_API.commonapp.models.consumer_category import get_consumer_category_by_id_string,get_category_by_tenant_id_string
from api.v1.smart360_API.commonapp.models.consumer_sub_category import get_sub_category_by_tenant_id_string
from api.v1.smart360_API.commonapp.models.frequency import get_frequency_by_tenant_id_string,get_frequency_by_id_string
from api.v1.smart360_API.lookup.models.camp_type import get_camp_type_by_tenant_id_string,get_camp_type_by_id_string
from api.v1.smart360_API.lookup.models.area import get_area_by_id_string
from api.v1.smart360_API.commonapp.models.sub_area import get_sub_area_by_id_string

from api.v1.smart360_API.commonapp.common_functions import get_payload,get_user,is_authorized,is_token_valid
from api.v1.smart360_API.smart360_API.messages import STATE,SUCCESS,ERROR,EXCEPTION,DATA
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
# Author: Priyanka Kachare
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
                    campaigns,total_pages, page_no = get_filtered_campaign(user, request)
                    # Code for filtering campaign end

                    # Code for lookups start
                    status = get_cam_status_by_tenant_id_string(user.tenant)
                    campaigns_type = get_camp_type_by_tenant_id_string(user.tenant.id_string)
                    category = get_category_by_tenant_id_string(user.tenant.id_string)
                    sub_category = get_sub_category_by_tenant_id_string(user.tenant.id_string)
                    frequency = get_frequency_by_tenant_id_string(user.tenant.id_string)
                    # Code for lookups end

                    # Code for sending campaigns in response
                    for campaign in campaigns:
                        campaign_list.append({
                            'cam_type': campaigns_type.objects.get(id = campaign.type_id).campaign_type,
                            'category': category.objects.get(id = campaign.category_id).category_name,
                            'sub_category': sub_category.objects.get(id= campaign.sub_category_id).sub_category_name,
                            'frequency':frequency.objects.get(id = campaign.frequency_id).frequency_name,
                            'status': status.objects.get(id = campaign.status_id).status_name,
                            'name':campaign.name,
                            'raised_on': campaign.created_date.strftime(DISPLAY_DATE_FORMAT),
                            'total_pages': total_pages,
                            'page_no': page_no
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
# API end Point: api/v1/campaign/
# API verb: GET, POST, PUT
# Package: Basic
# Modules: S&M
# Sub Module: Campaign
# Interaction: View Campaign and advertisment details, Add Campaign, Edit Campaign
# Usage: View, Add, Edit Campaign
# Tables used:  2.3.6 Campaign Master
# Auther: Priyanka
# Created on: 23/04/2020

# API for add, edit, view campaign details
class CampaignApiView(APIView):

    def get(self, request, format=None):
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
                    camp_id_string = request.data['camp_id_string']
                    campaign_obj = Campaign.objects.get(id_string=camp_id_string)
                    frequency_obj = get_frequency_by_id_string(campaign_obj.frequency_id)
                    camp_type_obj = get_camp_type_by_id_string(campaign_obj.type_id)
                    category_obj = get_consumer_category_by_id_string(campaign_obj.category_id)
                    area = get_area_by_id_string(campaign_obj.area_id)
                    sub_area = get_sub_area_by_id_string(campaign_obj.sub_area_id)
                    # Code for lookups end

                    # Code for sending campaign and advertisement details in response start
                    campaign_detail = {}
                    campaign_details = {
                        'camp_id': campaign_obj.id,
                        'camp_name': campaign_obj.name,
                        'frequency_id_string': frequency_obj.id_string,
                        'tenant_id_string': campaign_obj.tenant.id_string,
                        'utility_id_string': campaign_obj.utility.id_string,
                        'type_id_string': camp_type_obj.id_string,
                        'category_id_string': category_obj.id_string,
                        'area_id_string': area.id_string,
                        'sub_area_id_string': sub_area.id_string,
                        'start_date': campaign_obj.start_date,
                        'end_date': campaign_obj.end_date,
                        'description': campaign_obj.description if campaign_obj.description else '',
                        }
                    advertisements = Advertisements.objects.filter(campaign_id=camp_id_string)
                    advertisement_list = []
                    if advertisements:
                        for advertisement in advertisements:
                            advertisement_details = {
                                'advertisement_name': advertisement.name,
                                'description': advertisement.description,
                                'actual_amount': advertisement.actual_amount,
                                'start_date': advertisement.start_date,
                                'end_date': advertisement.end_date,
                                'area_id_string': area.id_string,
                                'sub_area_id_string': sub_area.id_string,
                                'category_id_string': category_obj.id_string,
                                'frequency_id_string': frequency_obj.id_string,
                            }
                            advertisement_list.append(advertisement_details)

                    campaign_detail['campaign_detail']=campaign_details
                    campaign_detail['cadvertisement_detail']=advertisement_list

                    return Response({
                            STATE: SUCCESS,
                            DATA: campaign_detail,
                        }, status=status.HTTP_200_OK)
                        # Code for sending campaign and advertisement details in response end
                else:
                    return Response({
                        STATE: ERROR,
                        DATA: '',
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                    DATA: '',
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                            campaign_details_list = {}
                            # save campaign details start
                            campaign_details = save_campaign_details(request, user)
                            # save campaign details end

                            if campaign_details:
                                # Request advertisement verification start
                                if is_advertisement_verified(request,user):
                                # Request advertisement verification end

                                    # save advertisement details start
                                    adv_details = save_advertisement_details(request,user,campaign_details.id_string)
                                    # save advertisement details end

                                    if adv_details:
                                        campaign_details_list['campaign_details'] = campaign_details
                                        campaign_details_list['adv_details'] = adv_details

                                        return Response({
                                            STATE: SUCCESS,
                                            'data':campaign_details_list,
                                        }, status=status.HTTP_200_OK)

                                    else:
                                        campaign_details_list['campaign_details'] = campaign_details
                                        campaign_details_list['adv_details'] = ''
                                        return Response({
                                            STATE: ERROR,
                                            'data': campaign_details_list,
                                        }, status=status.HTTP_400_BAD_REQUEST)

                                else:
                                    return Response({
                                        STATE: ERROR,
                                        'data': '',
                                    }, status=status.HTTP_400_BAD_REQUEST)

                            else:
                                return Response({
                                    STATE: ERROR,
                                    'data': '',
                                }, status=status.HTTP_400_BAD_REQUEST)

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

    def put(self, request, format=None):
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

                    # Request data verification start
                    if is_data_verified(request, user):
                    # Request data verification end

                        campaign_details_list = {}
                        campaign_id_string = request.data['cam_id_string']
                        # save updated values of campaign start
                        campaign_details = save_campaign_details(request, user)
                        # save updated values of campaign end

                        # Request advertisement verification start
                        if is_advertisement_verified(request, user):
                        # Request advertisement verification end

                            # save advertisement details start
                            adv_details = save_advertisement_details(request, user, campaign_id_string)
                            # save advertisement details end

                        campaign_details_list['campaign_details'] = campaign_details
                        campaign_details_list['adv_details'] = adv_details

                        return Response({
                            STATE: SUCCESS,
                            'data': campaign_details_list,
                        }, status=status.HTTP_200_OK)

                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





