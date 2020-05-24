from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, DATA, EXCEPTION
from v1.commonapp.models.frequency import Frequency, get_frequency_by_id_string
from v1.commonapp.serializers.frequency import FrequencySerializer,FrequencyViewSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination


class FrequencyList(generics.ListAPIView):
    serializer_class = FrequencySerializer
    pagination_class = StandardResultsSetPagination


    def get_queryset(self):
        queryset = Frequency.objects.filter(tenant=1, utility=1)
        return queryset


class FrequencyDetail(GenericAPIView):
    def get(self, request, id_string):
        try:
            frequency = get_frequency_by_id_string(id_string)
            if frequency:
                serializer = FrequencyViewSerializer(instance=frequency, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    DATA: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: '',
                }, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)