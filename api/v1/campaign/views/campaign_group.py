from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, DATA, EXCEPTION
from v1.campaign.models.campaign_group import get_camp_group_by_id_string,CampaignGroup
from v1.campaign.serializers.campaign_group import CampaignGroupListSerializer,CampaignGroupViewSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

# group/list/
class CampaignGroupList(generics.ListAPIView):
    serializer_class = CampaignGroupListSerializer
    pagination_class = StandardResultsSetPagination

    queryset = CampaignGroup.objects.filter(tenant=4, utility=1)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('name', 'tenant__id_string',)
    ordering_fields = ('name', 'tenant',)
    ordering = ('name',)  # always give by default alphabetical order
    search_fields = ('name', 'tenant__name',)



class CampaignGroupView(GenericAPIView):
    def get(self,request,id_string):
        try:
            campaign_group = get_camp_group_by_id_string(id_string)
            if campaign_group:
                serializer = CampaignGroupViewSerializer(instance=campaign_group, context={'request': request})
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
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
