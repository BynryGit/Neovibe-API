from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import STATE, SUCCESS, DATA, EXCEPTION
from v1.commonapp.serializers import status
from v1.commonapp.views.logger import logger
from v1.work_order.models.service_appointment_status import get_service_appointment_status_by_id_string
from v1.work_order.serializers.service_appointment_status import ServiceAppointmentStatus


class ServiceAppointmentStatus(GenericAPIView):

    def get(self, request, id_string):
        try:
            appointment_status = get_service_appointment_status_by_id_string(id_string)
            if appointment_status:
                serializer = ServiceAppointmentStatus(instance=appointment_status, context={'request': request})
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