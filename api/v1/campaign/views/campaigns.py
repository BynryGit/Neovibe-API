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
from v1.campaign.models.campaign_objective import get_cam_objective_by_id_string,get_cam_objective_by_id
from v1.campaign.models.campaign_group import get_camp_group_by_id
from v1.campaign.models.campaign_status import get_cam_status_by_tenant_id_string,get_cam_status_by_id_string
from v1.userapp.models.user_master import UserDetail
from v1.userapp.models.privilege import get_privilege_by_id
from v1.commonapp.models.sub_module import get_sub_module_by_id
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string,get_consumer_category_by_id,get_consumer_category_by_tenant_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_tenant_id_string

from v1.commonapp.models.frequency import get_frequency_by_tenant_id_string,get_frequency_by_id
from v1.commonapp.models.area import get_areas_by_tenant_id_string, get_area_by_id,get_area_by_id_string
from v1.commonapp.models.sub_area import get_sub_areas_by_tenant_id_string,get_sub_area_by_id
from v1.campaign.models.campaign import get_campaign_by_id_string

from v1.commonapp.common_functions import get_payload,get_user,is_authorized,is_token_valid
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA
from v1.campaign.models.campaign import Campaign

from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.campaign.models.campaign import Campaign as CampaignTbl
from v1.campaign.serializers.campaign import CampaignViewSerializer,CampaignListSerializer,AdvertismentViewSerializer

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
class CampaignList(generics.ListAPIView):
    serializer_class = CampaignListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        search_str = self.request.query_params.get('search', None)

        queryset = CampaignTbl.objects.filter(is_active=True).order_by('-id')

        utility_id_string = self.request.query_params.get('utility', None)
        category_id_string = self.request.query_params.get('category', None)
        sub_category_id_string = self.request.query_params.get('sub_category', None)
        area_id_string = self.request.query_params.get('area', None)
        sub_area_id_string = self.request.query_params.get('sub_area', None)
        object_id_string = self.request.query_params.get('object', None)
        status_id_string = self.request.query_params.get('status', None)

        if utility_id_string is not None:
            queryset = queryset.filter(utility__id_string=utility_id_string)
        if category_id_string is not None:
            category = get_consumer_category_by_id_string(category_id_string)
            queryset = queryset.filter(category_id=category.id)
        if sub_category_id_string is not None:
            sub_category = get_consumer_sub_category_by_id_string(sub_category_id_string)
            queryset = queryset.filter(sub_category_id=sub_category.id)
        if area_id_string is not None:
            area = get_area_by_id_string(area_id_string)
            queryset = queryset.filter(area_id=area.id)
        if sub_area_id_string is not None:
            sub_area = get_sub_area_by_id_string(sub_area_id_string)
            queryset = queryset.filter(sub_area_id=sub_area.id)
        if object_id_string is not None:
            objective = get_cam_objective_by_id_string(object_id_string)
            queryset = queryset.filter(objective_id=objective.id)
        if status_id_string is not None:
            status = get_cam_status_by_id_string(status_id_string)
            queryset = queryset.filter(status_id=status.id)

        if search_str is not None:
            queryset = CampaignTbl.objects.filter(is_active=True, name__icontains=search_str).order_by('-id')

        return queryset


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
class Campaigns(GenericAPIView):

    def get(self, request, id_string):
        try:
            campaign = get_campaign_by_id_string(id_string)
            if campaign:
                serializer = CampaignViewSerializer(instance=campaign, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    DATA: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: '',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def get(self, request,id_string):
    #     try:
    #         # Checking authentication start
    #         if is_token_valid(1):
    #             # payload = get_payload(request.headers['token'])
    #             # user = get_user(payload['id_string'])
    #             # Checking authentication end
    #
    #             # Checking authorization start
    #             if is_authorized():
    #                 # Checking authorization end
    #                 # Code for lookups start
    #                 advert = ''
    #                 campaign = ''
    #                 # campaign_obj = get_campaign_by_id_string(request.data['id_string'])
    #                 try:
    #                     advert = Advertisements.objects.get(id_string=id_string)
    #                 except:
    #                     campaign = Campaign.objects.get(id_string=id_string)
    #
    #                 if advert:
    #                     advertisement = get_advertisements_by_id_string(id_string=id_string)
    #                     objective = get_cam_objective_by_id(advertisement.objective_id)
    #                     group = get_camp_group_by_id(advertisement.group_id)
    #                     frequency_obj = get_frequency_by_id(advertisement.frequency_id)
    #                     area = get_area_by_id(advertisement.area_id)
    #                     sub_area = get_sub_area_by_id(advertisement.sub_area_id)
    #                     advertisement_detail = {
    #                         'advertisement_name': advertisement.name,
    #                         'description': advertisement.description,
    #                         'actual_amount': advertisement.actual_amount,
    #                         'budget_amount': advertisement.budget_amount,
    #                         'start_date': advertisement.start_date,
    #                         'end_date': advertisement.end_date,
    #                         'area_id_string': area.id_string,
    #                         'area': area.name,
    #                         'sub_area_id_string': sub_area.id_string,
    #                         'sub_area': sub_area.name,
    #                         'frequency_id_string': frequency_obj.id_string,
    #                         'frequency': frequency_obj.name,
    #                         'objective': objective.id_string,
    #                         'group': group.id_string,
    #                     }
    #                     return Response({
    #                         STATE: SUCCESS,
    #                         DATA: advertisement_detail,
    #                     }, status=status.HTTP_200_OK)
    #
    #                 if campaign:
    #                     campaign = get_campaign_by_id_string(id_string=id_string)
    #                     category_obj = get_consumer_category_by_id(campaign.category_id)
    #                     area = get_area_by_id(campaign.area_id)
    #                     sub_area = get_sub_area_by_id(campaign.sub_area_id)
    #                     objective = get_cam_objective_by_id(campaign.objective_id)
    #                     group = get_camp_group_by_id(campaign.group_id)
    #                     frequency_obj = get_frequency_by_id(campaign.frequency_id)
    #                 # Code for lookups end
    #
    #                 # Code for sending campaign and advertisement details in response start
    #
    #                     campaign_detail = {}
    #                     campaign_details = {
    #                         'camp_id': campaign.id,
    #                         'camp_name': campaign.name,
    #                         'frequency_id_string': frequency_obj.id_string,
    #                         'frequency': frequency_obj.name,
    #                         'tenant_id_string': campaign.tenant.id_string,
    #                         'tenant': campaign.tenant.name,
    #                         'utility_id_string': campaign.utility.id_string,
    #                         'utility': campaign.utility.name,
    #                         'category_id_string': category_obj.id_string,
    #                         'category': category_obj.name,
    #                         'area_id_string': area.id_string,
    #                         'area': area.name,
    #                         'sub_area_id_string': sub_area.id_string,
    #                         'sub_area': sub_area.name,
    #                         'start_date': campaign.start_date,
    #                         'end_date': campaign.end_date,
    #                         'description': campaign.description if campaign.description else '',
    #                         'group':group.id_string,
    #                         'objective': objective.id_string,
    #                     }
    #                     advertisements = Advertisements.objects.filter(campaign_id=campaign.id)
    #                     advertisement_list = []
    #                     if advertisements:
    #                         for advertisement in advertisements:
    #                             advertisement_details = {
    #                                 'advertisement_name': advertisement.name,
    #                                 'description': advertisement.description,
    #                                 'actual_amount': advertisement.actual_amount,
    #                                 'budget_amount': advertisement.budget_amount,
    #                                 'start_date': advertisement.start_date,
    #                                 'end_date': advertisement.end_date,
    #                                 'area_id_string': area.id_string,
    #                                 'area': area.name,
    #                                 'sub_area_id_string': sub_area.id_string,
    #                                 'sub_area': sub_area.name,
    #                                 'category_id_string': category_obj.id_string,
    #                                 'category': category_obj.name,
    #                                 'frequency_id_string': frequency_obj.id_string,
    #                                 'frequency': frequency_obj.name,
    #                             }
    #                             advertisement_list.append(advertisement_details)
    #
    #                     campaign_detail['campaign_detail'] = campaign_details
    #                     campaign_detail['advertisement_detail'] = advertisement_list
    #
    #                     return Response({
    #                         STATE: SUCCESS,
    #                         DATA: campaign_detail,
    #                     }, status=status.HTTP_200_OK)
    #                 # Code for sending campaign and advertisement details in response end
    #             else:
    #                 return Response({
    #                     STATE: ERROR,
    #                 }, status=status.HTTP_403_FORBIDDEN)
    #         else:
    #             return Response({
    #                 STATE: ERROR,
    #             }, status=status.HTTP_401_UNAUTHORIZED)
    #     except Exception as ex:
    #         return Response({
    #             STATE: EXCEPTION,
    #             ERROR: str(traceback.print_exc(ex))
    #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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




# API Header
# API end Point: api/v1/campaign/advert
# API verb: GET, POST, PUT
# Package: Basic
# Modules: S&M
# Sub Module: Campaign
# Interaction: View  advertisment details, Add advertisment, Edit advertisment
# Usage: View, Add, Edit advertisment
# Tables used:  2.3.6 Advertisment
# Auther: Priyanka
# Created on: 12/05/2020

# API for add, edit, view advertisment details
class Advertisment(GenericAPIView):

    def get(self, request, id_string):
        try:
            advert = get_advertisements_by_id_string(id_string=id_string)
            if advert:
                serializer = AdvertismentViewSerializer(instance=advert, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    DATA: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: '',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


