import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.settings import DISPLAY_DATE_FORMAT
from django.db import transaction
from v1.campaign.views.common_functions import get_filtered_campaign,is_data_verified,is_advertisement_verified,\
    save_advertisement_details,save_campaign_details,save_edited_basic_campaign_details,save_edited_basic_advertisement_details
from v1.userapp.models.user_master import UserDetail

from v1.campaign.models.advertisement import Advertisements,get_advertisements_by_id_string
from v1.campaign.models.campaign_status import get_cam_status_by_tenant_id_string
from v1.userapp.models.user_master import UserDetail
from v1.userapp.models.privilege import get_privilege_by_id
from v1.commonapp.models.sub_module import get_sub_module_by_id
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string,get_consumer_category_by_id,get_consumer_category_by_tenant_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_tenant_id_string

from v1.commonapp.models.frequency import get_frequency_by_tenant_id_string,get_frequency_by_id
from v1.commonapp.models.area import get_areas_by_tenant_id_string, get_area_by_id
from v1.commonapp.models.sub_area import get_sub_areas_by_tenant_id_string,get_sub_area_by_id
from v1.campaign.models.campaign import get_campaign_by_id_string

from v1.commonapp.common_functions import get_payload,get_user,is_authorized,is_token_valid
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA
from v1.campaign.models.campaign import Campaign

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
            if is_token_valid(1):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                # if is_authorized(user, privilege, sub_module):
                if is_authorized():
                # Checking authorization end

                    # Code for filtering campaign start
                    user = UserDetail.objects.get(id=2)
                    campaigns,total_pages, page_no, result, error = get_filtered_campaign(user, request)
                    if result == False:
                        return Response({
                            STATE: EXCEPTION,
                            ERROR: error
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    # Code for filtering campaign end

                    # Code for lookups start
                    statususe = get_cam_status_by_tenant_id_string(user.tenant.id_string)
                    categorys = get_consumer_category_by_tenant_id_string(user.tenant.id_string)
                    sub_category = get_consumer_sub_category_by_tenant_id_string(user.tenant.id_string)
                    frequencys = get_frequency_by_tenant_id_string(user.tenant.id_string)
                    # Code for lookups end

                    # Code for sending campaigns in response
                    for campaign in campaigns:
                        campaign_list.append({
                            'category': categorys.get(id=int(campaign.category_id)).name,
                            'sub_category': sub_category.get(id=int(campaign.sub_category_id)).name,
                            'frequency':frequencys.get(id =int(campaign.frequency_id)).name,
                            'status': statususe.get(id=int(campaign.status_id)).status,
                            'name':campaign.name,
                            'raised_on': campaign.created_date.strftime(DISPLAY_DATE_FORMAT),
                        })
                    campaign_list.append({
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
            if is_token_valid(1):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                # Checking authorization end

                    # Code for lookups start
                    # campaign_obj = get_campaign_by_id_string(request.data['id_string'])
                    campaign_obj = get_campaign_by_id_string('31950b44-6f5a-4551-9058-95f4bdddb08f')
                    frequency_obj = get_frequency_by_id(campaign_obj.frequency_id)
                    category_obj = get_consumer_category_by_id(campaign_obj.category_id)
                    area = get_area_by_id(campaign_obj.area_id)
                    sub_area = get_sub_area_by_id(campaign_obj.sub_area_id)
                    # Code for lookups end

                    # Code for sending campaign and advertisement details in response start
                    advertisement = get_advertisements_by_id_string('d27a1b29-552e-459d-9d8b-86407c260f03')
                    campaign_detail = {}
                    # advertisement = ""
                    if advertisement:
                        campaign_detail ={
                            'advertisement_name': advertisement.name,
                            'description': advertisement.description,
                            'actual_amount': advertisement.actual_amount,
                            'budget_amount': advertisement.budget_amount,
                            'start_date': advertisement.start_date,
                            'end_date': advertisement.end_date,
                            'area_id_string': area.id_string,
                            'sub_area_id_string': sub_area.id_string,
                            'category_id_string': category_obj.id_string,
                            'frequency_id_string': frequency_obj.id_string,
                        }

                    else:
                        campaign_details = {
                            'camp_id': campaign_obj.id,
                            'camp_name': campaign_obj.name,
                            'frequency_id_string': frequency_obj.id_string,
                            'tenant_id_string': campaign_obj.tenant.id_string,
                            'utility_id_string': campaign_obj.utility.id_string,
                            'category_id_string': category_obj.id_string,
                            'area_id_string': area.id_string,
                            'sub_area_id_string': sub_area.id_string,
                            'start_date': campaign_obj.start_date,
                            'end_date': campaign_obj.end_date,
                            'description': campaign_obj.description if campaign_obj.description else '',
                            }
                        advertisements = Advertisements.objects.filter(campaign_id=campaign_obj.id)
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
                        campaign_detail['advertisement_detail']=advertisement_list

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
            # if is_token_valid(request.data['token']):
            if is_token_valid(1):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
            # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                # Checking authorization end

                    # Code for add campaign start

                    # Request data verification start

                    user = UserDetail.objects.get(id=1)
                    if is_data_verified(request):
                    # Request data verification end

                        # check Campaign is Already Exists or not
                        # try:
                        #     if Campaign.objects.get(area_id=request.data['area'],sub_area_id=request.data['sub_area'],start_date=request.data['start_date'],end_date=request.data['end_date']):
                        #
                        #         campaign_data = {'campaign_name':request.data['campaign_name'],'area':request.data['area'],
                        #                          'sub_area':request.data['sub_area'],'start_date':request.data['start_date'],'end_date':request.data['end_date']}
                        #         return Response({
                        #             STATE: ERROR,
                        #             'data': campaign_data,
                        #         }, status=status.HTTP_409_CONFLICT)
                        # except:
                            campaign_details_list = {}
                            # save campaign details start
                            sid = transaction.savepoint()
                            campaign,result = save_campaign_details(request, user,sid)
                            if result == False:
                                return Response({
                                    STATE: EXCEPTION,
                                    ERROR: ERROR
                                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                            # save campaign details end
                            result,advertisement = save_advertisement_details(user,campaign,sid)
                            if result == True:
                                transaction.savepoint_commit(sid)
                                data = {
                                    "Message": "Data Save Successfully !"
                                }
                            else:
                                data = {
                                    "campaign_id_string": campaign.id_string
                                }
                            return Response({
                                STATE: SUCCESS,
                                DATA: data,
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

    def put(self, request, format=None):
        try:
            # Checking authentication start
            # if is_token_valid(request.data['token']):
            if is_token_valid(1):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
            # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                # if is_authorized(user, privilege, sub_module):
                if is_authorized():
                # Checking authorization end

                    # Request data verification start
                    if is_data_verified(request):
                    # Request data verification end

                        user = UserDetail.objects.get(id=2)
                        campaign, result = save_edited_basic_campaign_details(request, user)
                        if result == False:
                            return Response({
                                STATE: EXCEPTION,
                                ERROR: ERROR
                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                        result = save_edited_basic_advertisement_details(request, user)
                        if result == False:
                            return Response({
                                STATE: EXCEPTION,
                                ERROR: ERROR
                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                            data = {
                                "message ": "Update Sucessfully !"
                            }
                            return Response({
                                STATE: SUCCESS,
                                DATA: data,
                            }, status=status.HTTP_200_OK)
                            # Save basic details start
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





