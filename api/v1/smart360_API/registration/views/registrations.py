import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.smart360_API.registration.views.common_functions import is_token_valid, get_payload, \
    get_filtered_registrations, check_authorization, get_user

from api.v1.smart360_API.lookup.models.privillege import Privillege
from api.v1.smart360_API.lookup.models.sub_module import SubModule
from api.v1.smart360_API.smart360_API.settings import DISPLAY_DATE_FORMAT



# Api for getting registrations list, filter, search
class RegistrationListApiView(APIView):

    def get(self, request, format=None):
        try:
            registrations_list = []

            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
            # Checking authentication end

                # Checking authorization start
                privillege = Privillege.objects.filter(id = 1)
                sub_module = SubModule.objects.filter(id = 1)
                if check_authorization(user, privillege, sub_module):
                # Checking authorization end

                     # Code for filtering registrations start
                    registrations = get_filtered_registrations(user, request)
                    # Code for filtering registrations end

                    # Code for sending registrations in response start
                    for registration in registrations:
                        registrations_list.append({
                            'name' : registration.first_name + ' ' + registration.last_name,
                            'registration_no' : registration.registration_no,
                            'status' : Status.objects.get(id = registration.status_id).status,
                            'mobile_no' : registration.phone_no1,
                            'area' : Area.objects.get(id = registration.area_id).area,
                            'source' : SubArea.objects.get(id = registration.sub_area_id).sub_area,
                            'raised_on' : registration.registration_date.strftime(DISPLAY_DATE_FORMAT)
                        })
                    return Response({
                        'success': 'true',
                        'data': registrations_list,
                        'message': 'Data sent successfully.'
                    }, status=status.HTTP_200_OK)
                    # Code for sending registrations in response end

                else:
                    return Response({
                        'success': 'false',
                        'data': '',
                        'message': 'User does not have required privillege.',
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    'success': 'false',
                    'data': '',
                    'message': 'Please login first.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'success': 'false',
                'error': str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


