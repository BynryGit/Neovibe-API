
import logging
import traceback
from rest_framework.exceptions import APIException
from v1.commonapp.views.custom_exception import InvalidTokenException, InvalidAuthorizationException
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA,RESULTS
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from v1.commonapp.views.logger import logger
from v1.commonapp.views.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from v1.campaign.models.campaign import get_campaign_by_id_string
from v1.campaign.models.advertisement import Advertisements,get_advertisements_by_id_string
from v1.campaign.serializers.advertisment import AdvertismentViewSerializer,AdvertismentListSerializer,AdvertisementSerializer
from v1.commonapp.common_functions import is_token_valid, get_payload, get_user, is_authorized
from v1.campaign.views.common_functions import is_data_verified
from v1.userapp.models.user_master import UserDetail

# API Header
# API end Point: api/v1/campaign/:id_string/adverts-list
# API verb: GET
# Package: Basic
# Modules: S&M
# Sub Module: Campaign
# Interaction: View  advertisment list
# Usage: View
# Tables used:  2.3.6 Advertisment
# Auther: Priyanka
# Created on: 12/05/2020

# API for  view advertisment list

class AdvertismentList(generics.ListAPIView):
    try:
        serializer_class = AdvertismentListSerializer
        pagination_class = StandardResultsSetPagination

        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filter_fields = ('name', 'start_date',)
        ordering_fields = ('name',)
        ordering = ('created_date',)  # always give by default alphabetical order
        search_fields = ('name',)

        def get_queryset(self):
            if is_token_valid(1):
                if is_authorized():
                    queryset = ''
                    campaign = get_campaign_by_id_string(self.kwargs['id_string'])
                    if campaign:
                        queryset = Advertisements.objects.filter(campaign_id=campaign.id, is_active=True)
                    return queryset
                else:
                    raise InvalidAuthorizationException
            else:
                raise InvalidTokenException

    except Exception as ex:
        logger().log(ex, 'ERROR')
        raise APIException

# API Header
# API end Point: api/v1/campaign/id_string/advertisement
# API verb: POST
# Package: Basic
# Modules: S&M
# Sub Module: Campaign
# Interaction: Add  advertisment details
# Usage: Add advertisment
# Tables used:  2.3.6 Advertisment
# Auther: Priyanka
# Created on: 18/05/2020

# API for  add advertisment details
class Advertisement(GenericAPIView):
    def post(self, request, id_string):
        try:
            if is_token_valid(1):
                if is_authorized():
                    if is_data_verified(request):
                        user = UserDetail.objects.get(id=5)
                        campaign_obj = get_campaign_by_id_string(id_string)
                        serializer = AdvertisementSerializer(data=request.data)
                        if serializer.is_valid():
                            advertisement = serializer.create(serializer.validated_data,user,campaign_obj)
                            serializer = AdvertismentViewSerializer(instance=advertisement, context={'request': request})
                            return Response({
                                STATE: SUCCESS,
                                DATA: serializer.data,
                            }, status=status.HTTP_200_OK)
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
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# API Header
# API end Point: api/v1/campaign/advert/:id_string
# API verb: GET
# Package: Basic
# Modules: S&M
# Sub Module: Campaign
# Interaction: View  advertisment details
# Usage: View advertisment
# Tables used:  2.3.6 Advertisment
# Auther: Priyanka
# Created on: 12/05/2020

# API for  view advertisment details
class AdvertismentDetail(GenericAPIView):

    def get(self, request, id_string):
        try:
            advert = get_advertisements_by_id_string(id_string=id_string)
            if advert:
                serializer = AdvertismentViewSerializer(instance=advert, context={'request': request})
                return Response({
                    STATE: SUCCESS,
                    DATA: serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: '',
                }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id_string):
        try:
            # Checking authentication start
            if is_token_valid(1):
                # Checking authentication end

                # Checking authorization start
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    if is_data_verified(request):
                        # Request data verification end

                        # Save basic details start
                        user = UserDetail.objects.get(id=2)
                        advert_obj = get_advertisements_by_id_string(id_string)
                        if advert_obj:
                            serializer = AdvertisementSerializer(data=request.data)
                            if serializer.is_valid():
                                advert_obj = serializer.update(advert_obj, serializer.validated_data, user)
                                view_serializer = AdvertismentViewSerializer(instance=advert_obj,
                                                                         context={'request': request})
                                return Response({
                                    STATE: SUCCESS,
                                    RESULTS: view_serializer.data,
                                }, status=status.HTTP_200_OK)
                            else:
                                return Response({
                                    STATE: ERROR,
                                    RESULTS: serializer.errors,
                                }, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({
                                STATE: ERROR,
                            }, status=status.HTTP_404_NOT_FOUND)
                        # Save basic details start
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
            logger().log(e, 'ERROR', user='test', name='test')
            return Response({
                STATE: EXCEPTION,
                ERROR: ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






