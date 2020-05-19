from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import EXCEPTION, STATE, ERROR, RESULTS, SUCCESS
from v1.commonapp.common_functions import is_authorized, is_token_valid
from v1.commonapp.views.logger import logger
from v1.consumer.serializers.consumer import ConsumerSerializer, ConsumerViewSerializer
from v1.registration.views.common_functions import is_data_verified
from v1.userapp.models.user_master import UserDetail


class Consumer(GenericAPIView):

    def post(self, request):
        try:
            # Checking authentication start
            if is_token_valid(request.headers['token']):
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    user = UserDetail.objects.get(id = 2)
                    if is_data_verified(request):
                    # Request data verification end
                        serializer = ConsumerSerializer(data=request.data)
                        if serializer.is_valid():
                            consumer_obj = serializer.create(serializer.validated_data, user)
                            view_serializer = ConsumerViewSerializer(instance=consumer_obj, context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                RESULTS: view_serializer.data,
                            }, status=status.HTTP_201_CREATED)
                        else:
                            return Response({
                                STATE: ERROR,
                                RESULTS: serializer.errors,
                            }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            STATE: ERROR,
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        STATE: ERROR,
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            # logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                ERROR: ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)