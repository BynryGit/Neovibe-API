from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, DATA, EXCEPTION
from v1.campaign.models.advert_status import AdvertStatus,get_advert_status_by_id_string
from v1.campaign.serializers.advertisement_status import AdvertisementStatusListSerializer,AdvertisementStatusViewSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class AdvertisementStatusList(generics.ListAPIView):
    serializer_class = AdvertisementStatusListSerializer
    pagination_class = StandardResultsSetPagination

    queryset = AdvertStatus.objects.filter(tenant=4, utility=1)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('name', 'tenant__id_string',)
    ordering_fields = ('name', 'tenant',)
    ordering = ('name',)  # always give by default alphabetical order
    search_fields = ('name', 'tenant__name',)



class AdvertisementStatusView(GenericAPIView):
    def get(self,request,id_string):
        try:
            advert_status = get_advert_status_by_id_string(id_string)
            if advert_status:
                serializer = AdvertisementStatusViewSerializer(instance=advert_status,context={'request':request})
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
