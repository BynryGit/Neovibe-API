import traceback
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status

from v1.campaign.models.campaign_objective import get_cam_objective_by_id_string,get_cam_objective_by_id
from v1.campaign.models.campaign_status import get_cam_status_by_tenant_id_string,get_cam_status_by_id_string
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string,get_consumer_category_by_id,get_consumer_category_by_tenant_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.commonapp.models.area import get_areas_by_tenant_id_string, get_area_by_id,get_area_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.campaign.models.campaign import get_campaign_by_id_string
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.campaign.models.campaign import Campaign as CampaignTbl
from v1.campaign.serializers.campaign import CampaignViewSerializer,CampaignListSerializer

# API Header
# API end Point: api/v1/campaign
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
# API end Point: api/v1/campaign/:id_string
# API verb: GET
# Package: Basic
# Modules: S&M
# Sub Module: Campaign
# Interaction: View Campaign
# Usage: View
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



