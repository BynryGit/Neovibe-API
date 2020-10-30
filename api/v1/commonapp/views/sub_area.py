from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, DATA, EXCEPTION
from v1.commonapp.common_functions import is_token_valid, is_authorized
from v1.commonapp.models.sub_area import SubArea, get_sub_area_by_id_string
from v1.commonapp.serializers.sub_area import SubAreaListSerializer, SubAreaViewSerializer
from v1.commonapp.views.custom_exception import CustomAPIException, InvalidAuthorizationException, InvalidTokenException
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.utility.models.utility_master import get_utility_by_id_string


class SubAreaList(generics.ListAPIView):
    try:
        serializer_class = SubAreaListSerializer

        def get_queryset(self):
            response, user_obj = is_token_valid(self.request.headers['Authorization'])
            if response:
                if is_authorized(1,1,1,user_obj):
                    utility = get_utility_by_id_string(self.kwargs['id_string'])
                    queryset = SubArea.objects.filter(utility = utility, is_active = True)
                    if queryset:
                        return queryset
                    else:
                        raise CustomAPIException("Sub areas not found.", status.HTTP_404_NOT_FOUND)
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException
    except Exception as e:
        logger().log(e, 'MEDIUM', module = 'Commonapp', sub_module = 'Commonapp')


class SubAreaDetail(GenericAPIView):
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