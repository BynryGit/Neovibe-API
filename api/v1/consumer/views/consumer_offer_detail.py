from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.messages import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import get_user_from_token
from v1.commonapp.views.logger import logger
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.consumer.serializers.consumer_offer_detail import ConsumerOfferDetailSerializer
from v1.userapp.decorators import is_token_validate

# API Header
# API end Point: api/v1/consumer/:id_string/offer-detail
# API verb: POST
# Package: Basic
# Modules: S&M, Consumer Care, Consumer Ops
# Sub Module: Consumer
# Interaction: Add consumer offer detail
# Usage: Add
# Tables used: Consumer offer detail
# Author: Rohan
# Created on: 25/01/2021


class ConsumerOfferDetail(GenericAPIView):

    @is_token_validate
    # @role_required(CONSUMER_OPS, CONSUMER_OPS_CONSUMER, EDIT)
    def post(self, request, id_string):
        try:
            user_id_string = get_user_from_token(request.headers['Authorization'])
            user = get_user_by_id_string(user_id_string)
            consumer = get_consumer_by_id_string(id_string)
            serializer = ConsumerOfferDetailSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                consumer_offer_detail = serializer.create(serializer.validated_data, consumer, user)
                view_serializer = ConsumerOfferDetailSerializer(instance=consumer_offer_detail, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    RESULT: view_serializer.data,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    STATE: ERROR,
                    RESULT: list(serializer.errors.values())[0][0],
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger().log(e, 'HIGH', module='Consumer Ops', sub_module='Consumer')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)