from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import STATE, SUCCESS, DATA, EXCEPTION
from v1.commonapp.serializers import status
from v1.commonapp.views.logger import logger
from v1.registration.models.registration_status import get_registration_status_by_id_string
from v1.registration.serializers.registration import RegistrationStatusViewSerializer


class RegistrationStatus(GenericAPIView):

    def get(self, request, id_string):
        try:
            registration_status = get_registration_status_by_id_string(id_string)
            if registration_status:
                serializer = RegistrationStatusViewSerializer(instance=registration_status, context={'request': request})
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

    def post(self, request):
        try:
            pass
        except Exception as e:
            pass

    def put(self, request):
        try:
            pass
        except Exception as e:
            pass