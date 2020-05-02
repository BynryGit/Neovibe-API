import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.settings import DISPLAY_DATE_FORMAT
from v1.registration.models.survey import Survey, get_registration_by_id_string
from v1.commonapp.common_functions import is_token_valid, get_payload, get_user, is_authorized
from v1.commonapp.models.sub_module import get_sub_module_by_id
from v1.commonapp.models.Survey import get_survey_by_id_string
from v1.commonapp.models.survey_status import get_survey_status_by_id_string,get_survey_status_by_id
from v1.commonapp.models.survey_objective import get_survey_objective_by_id_string
from v1.commonapp.models.survey_type import get_survey_type_by_id_string,get_survey_type_by_id
from v1.commonapp.models.area import get_area_by_id,get_areas_by_tenant_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id,get_sub_areas_by_tenant_id_string
from v1.survey.views.common_functions import get_filtered_location_survey,get_filtered_consumer_survey,\
    is_data_verified,save_location_survey_details,get_consumer_survey_list,is_consumer_data_verified,save_consumer_survey_details,\
    save_consumer_details,is_assignment_verified,save_vendor_assignment_details,get_vendor_details
from v1.userapp.models.privilege import get_privilege_by_id
from api.messages import SUCCESS,STATE,ERROR,EXCEPTION,DATA



# API Header
# API end Point: api/v1/survey/list
# API verb: GET
# Package: Basic
# Modules: S&M
# Sub Module: Survey
# Interaction: Survey list
# Usage: API will fetch required data for Location and consumer Survey list
# Tables used: 2.3.1 Survey Master,2.3.4 Survey Consumer
# Author: Priyanka
# Created on: 28/04/2020


# API for getting list data of Location Survey
class SurveyListApiView(APIView):

    def get(self, request, format=None):
        try:
            # Initializing output list start
            survey_list = []
            # Initializing output list end

            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                privilege = get_privilege_by_id(1)
                sub_module = get_sub_module_by_id(1)
                if is_authorized(user, privilege, sub_module):
                    # Checking authorization end

                    if request.data['type_id'] == "Location":

                        # Code for filtering location survey start
                        surveys, total_pages, page_no = get_filtered_location_survey(user, request)
                        # Code for filtering location survey end

                        # Code for lookups start
                        status = get_survey_status_by_id_string(user.tenant.id_string)
                        type = get_survey_type_by_id_string(user.tenant.id_string)
                        objective = get_survey_type_by_id(user.tenant.id_string)
                        areas = get_areas_by_tenant_id_string(user.tenant.id_string)
                        sub_areas = get_sub_areas_by_tenant_id_string(user.tenant.id_string)
                        # Code for lookups end

                        # Code for sending location survey in response start
                        for survey in surveys:
                            survey_list.append({
                                'survey_id':survey.id,
                                'name': survey.name,
                                'objective': objective.objects.get(id_string=survey.objective).objective,
                                'status': status.objects.get(id_string=survey.status).status_name,
                                'area': areas.objects.get(id_string=survey.area).area_name,
                                'sub_area': sub_areas.objects.get(id_string=survey.sub_area).sub_area_name,
                                'type': type.objects.get(id_string=survey.type).name,
                                'start_date':survey.start_date,
                                'end_date':survey.end_date,
                                'total_pages': total_pages,
                                'page_no': page_no
                            })
                        # Code for sending location survey in response end

                    else:
                        # Code for filtering consumer survey start
                        surveys, total_pages, page_no = get_filtered_consumer_survey(user, request)
                        # Code for filtering consumer survey end

                        # Code for lookups start
                        status = get_survey_status_by_id_string(user.tenant.id_string)
                        type = get_survey_type_by_id_string(user.tenant.id_string)
                        objective = get_survey_objective_by_id_string(user.tenant.id_string)
                        areas = get_areas_by_tenant_id_string(user.tenant.id_string)
                        sub_areas = get_sub_areas_by_tenant_id_string(user.tenant.id_string)
                        # Code for lookups end

                        # Code for sending consumer survey in response start
                        for consumer_survey in surveys:
                            survey_list.append({
                                'survey_id': consumer_survey.survey_id.id,
                                'name': consumer_survey.name,
                                'consumer_no': consumer_survey.consumer_no,
                                'mobile_no': consumer_survey.mobile_no,
                                'no_of_consumers': consumer_survey.no_of_consumers,
                                'objective': objective.objects.get(id_string=consumer_survey.objective).objective,
                                'status': status.objects.get(id_string=consumer_survey.status).status_name,
                                'area': areas.objects.get(id_string=consumer_survey.area).area_name,
                                'sub_area': sub_areas.objects.get(id_string=consumer_survey.sub_area).sub_area_name,
                                'type': type.objects.get(id_string=consumer_survey.type).name,
                                'start_date': consumer_survey.start_date,
                                'end_date': consumer_survey.end_date,
                                'total_pages': total_pages,
                                'page_no': page_no
                            })
                        # Code for sending consumer survey in response end

                    return Response({
                        STATE: SUCCESS,
                        DATA: survey_list,
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({
                        STATE: ERROR,
                        DATA: '',
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                    DATA: '',
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# API Header
# API end Point: api/v1/survey=?id-string
# API verb: GET, POST, PUT
# Package: Basic
# Modules: S&M
# Sub Module: Location Survey
# Interaction: View Location Survey, Add Location Survey, Edit Location Survey
# Usage: View, Add, Edit Location Survey
# Tables used: 2.3.1 Survey Master
# Auther: Priyanka
# Created on: 29/04/2020

class LocationSurveyApiView(APIView):

    def get(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                privilege = get_privilege_by_id(1)
                sub_module = get_sub_module_by_id(1)
                if is_authorized(user, privilege, sub_module):
                    # Checking authorization end

                    # Code for lookups start
                    survey = get_survey_by_id_string(request.data['id_string'])
                    area = get_area_by_id(survey.area)
                    sub_area = get_sub_area_by_id(survey.sub_area)
                    type = get_survey_type_by_id(survey.type)
                    objective = get_survey_type_by_id(survey.objective)
                    status = get_survey_status_by_id(survey.status)

                    # Code for lookups end

                    # Code for sending Location Survey in response start
                    data = {
                        'tenant_id_string': survey.tenant.id_string,
                        'utility_id_string': survey.utility.id_string,
                        'name':survey.name,
                        'objective':objective.id_string,
                        'discription':survey.description,
                        'type':type.id_string,
                        'start_date': survey.start_date.strftime(DISPLAY_DATE_FORMAT),
                        'end_date': survey.end_date.strftime(DISPLAY_DATE_FORMAT),
                        'completion_date': survey.completion_date.strftime(DISPLAY_DATE_FORMAT),
                        'area_id_string': area.id_string,
                        'sub_area_id_string': sub_area.id_string,
                        'is_active': survey.is_active,
                        'status':status.id_string,
                    }
                    return Response({
                        STATE: SUCCESS,
                        DATA: data,
                    }, status=status.HTTP_200_OK)
                    # Code for sending Location Survey in response end

                else:
                    return Response({
                        STATE: ERROR,
                        DATA: '',
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                    DATA: '',
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                privilege = get_privilege_by_id(1)
                sub_module = get_sub_module_by_id(1)
                if is_authorized(user, privilege, sub_module):
                    # Checking authorization end

                    # Request data verification start
                    if is_data_verified(request, user):
                        # Request data verification end

                        # check Survey is Already Exists or not
                        if Survey.objects.get(name=request.data['survey_name'],area=request.data['area'],sub_area=request.data['sub_area'],
                                            start_date=request.data['start_date'],end_date=request.data['end_date']):

                            survey_data = {'survey_name':request.data['survey_name'],'area':request.data['area'],'sub_area':request.data['sub_area'],\
                                            'start_date':request.data['start_date'],'end_date':request.data['end_date']}

                            return Response({
                                STATE: ERROR,
                                'data': survey_data,
                            }, status=status.HTTP_409_CONFLICT)

                        else:
                            # Save Location Survey start
                            location_survey = save_location_survey_details(request, user)
                            # Save Location Survey start

                            return Response({
                                STATE: SUCCESS,
                                DATA: location_survey,
                            }, status=status.HTTP_200_OK)
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
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                privilege = get_privilege_by_id(1)
                sub_module = get_sub_module_by_id(1)
                if is_authorized(user, privilege, sub_module):
                    # Checking authorization end

                    # Request data verification start
                    if is_data_verified(request, user):
                        # Request data verification end

                        # Update Location Survey start
                        location_survey = save_location_survey_details(request, user)
                        # Update Location Survey start

                        return Response({
                            STATE: SUCCESS,
                            DATA: location_survey,
                        }, status=status.HTTP_200_OK)
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
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# API Header
# API end Point: api/v1/consumer-survey/
# API verb: GET, POST, PUT
# Package: Basic
# Modules: S&M
# Sub Module: Consumer Survey
# Interaction: View Consumer Survey, Add Consumer Survey, Edit Consumer Survey
# Usage: View, Add, Edit Consumer Survey
# Tables used: 2.3.1 Survey Master,2.3.4 Survey Consumer
# Auther: Priyanka
# Created on: 29/04/2020

class ConsumerSurveyApiView(APIView):

    def get(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                privilege = get_privilege_by_id(1)
                sub_module = get_sub_module_by_id(1)
                if is_authorized(user, privilege, sub_module):
                    # Checking authorization end

                    if request.data['consumer_id_string']:
                        # Code for lookups start
                        survey = get_survey_by_id_string(request.data['consumer_id_string'])
                        area = get_area_by_id(survey.area)
                        sub_area = get_sub_area_by_id(survey.sub_area)
                        type = get_survey_type_by_id(survey.type)
                        objective = get_survey_type_by_id(survey.objective)
                        status = get_survey_status_by_id(survey.status)
                        # Code for lookups end

                        # Code for sending Consumer Survey in response start
                        data = {
                            'tenant_id_string': survey.tenant.id_string,
                            'utility_id_string': survey.utility.id_string,
                            'name':survey.name,
                            'objective':objective.id_string,
                            'discription':survey.description,
                            'type':type.id_string,
                            'no_of_consumers':survey.no_of_consumers,
                            'start_date': survey.start_date.strftime(DISPLAY_DATE_FORMAT),
                            'end_date': survey.end_date.strftime(DISPLAY_DATE_FORMAT),
                            'completion_date': survey.completion_date.strftime(DISPLAY_DATE_FORMAT),
                            'area_id_string': area.id_string,
                            'sub_area_id_string': sub_area.id_string,
                            'is_active': survey.is_active,
                            'status':status.id_string,
                        }

                        return Response({
                            STATE: SUCCESS,
                            DATA: data,
                        }, status=status.HTTP_200_OK)
                        # Code for sending Consumer Survey in response end
                    else:
                        data = get_consumer_survey_list(request,user)
                        return Response({
                            STATE: SUCCESS,
                            DATA: data,
                        }, status=status.HTTP_200_OK)
                        # Code for sending Consumer Survey in response end
                else:
                    return Response({
                        STATE: ERROR,
                        DATA: '',
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                    DATA: '',
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                privilege = get_privilege_by_id(1)
                sub_module = get_sub_module_by_id(1)
                if is_authorized(user, privilege, sub_module):
                    # Checking authorization end

                    # Request data verification start
                    if is_consumer_data_verified(request, user):
                        # Request data verification end

                        # check Survey is Already Exists or not
                        if Survey.objects.get(name=request.data['survey_name'],area=request.data['area'],sub_area=request.data['sub_area'],
                                            start_date=request.data['start_date'],end_date=request.data['end_date']):

                            survey_data = {'survey_name':request.data['survey_name'],'area':request.data['area'],'sub_area':request.data['sub_area'],\
                                            'start_date':request.data['start_date'],'end_date':request.data['end_date']}

                            return Response({
                                STATE: ERROR,
                                'data': survey_data,
                            }, status=status.HTTP_409_CONFLICT)

                        else:
                            survey_list = {}
                            # Save Consumer Survey start
                            consumer_survey = save_consumer_survey_details(request, user)

                            # save all consumer details
                            consumer_details = []
                            if consumer_survey and request.data['consumer_datas']:
                                consumer_details = save_consumer_details(request, user,consumer_survey)

                            # Save Consumer Survey end
                            survey_list['consumer_survey'] = consumer_survey
                            survey_list['consumer_details'] = consumer_details

                            return Response({
                                STATE: SUCCESS,
                                DATA: survey_list,
                            }, status=status.HTTP_200_OK)
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
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                privilege = get_privilege_by_id(1)
                sub_module = get_sub_module_by_id(1)
                if is_authorized(user, privilege, sub_module):
                    # Checking authorization end

                    # Request data verification start
                    if is_consumer_data_verified(request, user):
                        # Request data verification end
                        survey_list = {}
                        # Update Consumer Survey start
                        consumer_survey = save_consumer_survey_details(request, user)
                        # Update Consumer Survey start

                        consumer_details = []
                        if consumer_survey and request.data['consumer_datas']:
                            consumer_details = save_consumer_details(request, user, consumer_survey)

                        survey_list['consumer_survey'] = consumer_survey
                        survey_list['consumer_details'] = consumer_details


                        return Response({
                            STATE: SUCCESS,
                            DATA: survey_list,
                        }, status=status.HTTP_200_OK)
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
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API Header
# API end Point: api/v1/assign-vendor/
# API verb: GET, POST
# Package: Basic
# Modules: S&M
# Sub Module: Assign Vendor
# Interaction: View vendor list , Assign vendor
# Usage: View, Assign vendor
# Tables used: 2.3.2 Survey Assignment
# Auther: Priyanka
# Created on: 30/04/2020

class AssignVendorApiView(APIView):

    def get(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                privilege = get_privilege_by_id(1)
                sub_module = get_sub_module_by_id(1)
                if is_authorized(user, privilege, sub_module):
                 # Checking authorization end
                    print()
                    vendor_details = get_vendor_details(request,user)
                else:
                    return Response({
                        STATE: ERROR,
                        DATA: '',
                    }, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    STATE: ERROR,
                    DATA: '',
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                privilege = get_privilege_by_id(1)
                sub_module = get_sub_module_by_id(1)
                if is_authorized(user, privilege, sub_module):
                    # Checking authorization end

                    # Request data verification start
                    if is_assignment_verified(request, user):
                        # Request data verification end

                        # save assignment details start
                        assign_vendor = save_vendor_assignment_details(request, user)
                        # save assignment details end

                        return Response({
                            STATE: SUCCESS,
                            DATA: assign_vendor,
                        }, status=status.HTTP_200_OK)
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
            return Response({
                STATE: EXCEPTION,
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

