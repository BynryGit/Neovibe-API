from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, DATA, EXCEPTION
from v1.commonapp.models.area import Area, get_area_by_id_string
from v1.commonapp.serializers.area import AreaViewSerializer, AreaListSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination


class AreaList(generics.ListAPIView):
    serializer_class = AreaListSerializer
    pagination_class = StandardResultsSetPagination


    def get_queryset(self):
        queryset = Area.objects.filter(tenant=user.tenant, utility=user.uitility)
        return queryset


class AreaView(GenericAPIView):
    def get(self, request, id_string):
        try:
            area = get_area_by_id_string(id_string)
            if area:
                serializer = AreaViewSerializer(instance=area, context={'request': request})
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