from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import get_user_from_token
from v1.commonapp.views.logger import logger
from v1.consumer.serializers.consumer_feedback import ConsumerFeedbackSerializer, ConsumerFeedbackListSerializer
from v1.userapp.decorators import is_token_validate


class ConsumerFeedback(GenericAPIView):
    @is_token_validate
    # #role_required(ADMIN, UTILITY_MASTER, EDIT)
    def post(self, request):
        print("$$$$$$$$$$$$$$$$$$$$$",request)
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            serializer = ConsumerFeedbackSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                obj = serializer.create(serializer.validated_data, user)
                view_serializer = ConsumerFeedbackListSerializer(instance=obj, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULTS: view_serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: ERROR,
                    RESULTS: list(serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module='Cx', sub_module='Consumer')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULTS: str(e),
            }, status=res.status_code)