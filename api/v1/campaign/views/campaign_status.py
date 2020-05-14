from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, DATA, EXCEPTION
from v1.campaign.models.campaign_status import CampaignStatus,get_cam_status_by_id_string
from v1.campaign.serializers.campaign_status import CampaignStatusListSerializer,CampaignStatusViewSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

# campaign-status/list/
class CampaignstatusList(generics.ListAPIView):
    serializer_class = CampaignStatusListSerializer
    pagination_class = StandardResultsSetPagination

    queryset = CampaignStatus.objects.filter(tenant=1, utility=1)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('name', 'tenant__id_string',)
    ordering_fields = ('name', 'tenant',)
    ordering = ('name',)  # always give by default alphabetical order
    search_fields = ('name', 'tenant__name',)



class CampaignStatusView(GenericAPIView):
    def get(self,request,id_string):
        try:
            campaign_status = get_cam_status_by_id_string(id_string)
            if campaign_status:
                serializer = CampaignStatusViewSerializer(instance=campaign_status,context={'request':request})
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
