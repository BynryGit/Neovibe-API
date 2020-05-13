import traceback
from rest_framework.response import Response
from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DATA
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status

from v1.campaign.models.campaign import get_campaign_by_id_string
from v1.campaign.models.advertisement import Advertisements,get_advertisements_by_id_string
from v1.campaign.serializers.advertisment import AdvertismentViewSerializer,AdvertismentListSerializer


# API Header
# API end Point: api/v1/campaign/:id_string/adverts
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
class AdvertismentList(GenericAPIView):

    def get(self, request, id_string):
        try:
            campaign = get_campaign_by_id_string(id_string)
            if campaign:
                advert_obj = Advertisements.objects.filter(campaign_id=campaign.id,is_active=True)
                if advert_obj:
                    serializer = AdvertismentListSerializer(instance=advert_obj, many=True,context={'request': request})
                    return Response({
                        STATE: SUCCESS,
                        DATA: serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: EXCEPTION,
                        DATA: '',
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({
                    STATE: EXCEPTION,
                    DATA: '',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# API Header
# API end Point: api/v1/campaign/advert/:id_string
# API verb: GET, POST, PUT
# Package: Basic
# Modules: S&M
# Sub Module: Campaign
# Interaction: View  advertisment details, Add advertisment, Edit advertisment
# Usage: View, Add, Edit advertisment
# Tables used:  2.3.6 Advertisment
# Auther: Priyanka
# Created on: 12/05/2020

# API for add, edit, view advertisment details
class Advertisment(GenericAPIView):

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
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


