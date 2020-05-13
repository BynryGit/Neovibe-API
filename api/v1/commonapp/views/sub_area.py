from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, DATA, EXCEPTION
from v1.commonapp.models.sub_area import SubArea, get_sub_area_by_id_string
from v1.commonapp.serializers.sub_area import SubAreaListSerializer, SubAreaViewSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination


class SubAreaList(generics.ListAPIView):
    serializer_class = SubAreaListSerializer
    pagination_class = StandardResultsSetPagination


    def get_queryset(self):
        queryset = SubArea.objects.filter(tenant=user.tenant, utility=user.uitility)
        return queryset


class SubAreaView(GenericAPIView):
    def get(self, request, id_string):
        try:
            sub_area = get_sub_area_by_id_string(id_string)
            if sub_area:
                serializer = SubAreaViewSerializer(instance=sub_area, context={'request': request})
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