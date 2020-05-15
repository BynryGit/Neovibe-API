
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, DATA, EXCEPTION
from v1.campaign.serializers.campaign_objective import ObjectiveListSerializer,ObjectiveViewSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.campaign.models.campaign_objective import CampaignObjective,get_cam_objective_by_id_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.commonapp.views.logger import logger

# objective/list
class CampaignObjectiveList(generics.ListAPIView):
    serializer_class = ObjectiveListSerializer
    pagination_class = StandardResultsSetPagination

    queryset = CampaignObjective.objects.filter(tenant=1, utility=1)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('name', 'tenant__id_string',)
    ordering_fields = ('name', 'tenant',)
    ordering = ('name',)  # always give by default alphabetical order
    search_fields = ('name', 'tenant__name',)



class CampaignObjectiveDetail(GenericAPIView):

    def get(self,request,id_string):
        try:
            campaign_obj = get_cam_objective_by_id_string(id_string)
            if campaign_obj:
                serializer = ObjectiveViewSerializer(instance=campaign_obj,context={'request': request})
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
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)