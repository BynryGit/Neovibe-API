import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from api.settings import DISPLAY_DATE_FORMAT
from v1.consumer.models.consumer_category import get_consumer_category_by_id
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id
from v1.userapp.models.user_master import UserDetail
from v1.consumer.models.consumer_category import get_consumer_category_by_tenant_id_string,get_consumer_category_by_id_string
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_tenant_id_string,get_consumer_sub_category_by_id_string
from v1.supplier.models.supplier_master import get_supplier_by_tenant_id_string
from v1.commonapp.common_functions import is_token_valid, get_payload, get_user, is_authorized
from v1.commonapp.models.sub_module import get_sub_module_by_id
from v1.survey.models.survey import get_survey_by_id_string,get_survey_by_tenant_id_string,Survey
from v1.survey.models.survey_consumer import get_survey_consumer_by_id_string,SurveyConsumer
from v1.survey.models.survey_status import get_survey_status_by_id_string,get_survey_status_by_id,get_survey_status_by_tenant_id_string
from v1.survey.models.survey_objective import get_survey_objective_by_tenant_id_string
from v1.survey.models.survey_type import get_survey_type_by_id_string,get_survey_type_by_id,get_survey_type_by_tenant_id_string
from v1.commonapp.models.area import get_area_by_id,get_areas_by_tenant_id_string,get_area_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id,get_sub_areas_by_tenant_id_string,get_sub_area_by_id_string
from v1.survey.views.common_functions import get_filtered_location_survey,get_filtered_consumer_survey,\
    is_data_verified,save_survey_details,get_consumer_survey_list,is_consumer_data_verified,save_consumer_survey_details,\
    save_consumer_details,is_assignment_verified,save_vendor_assignment_details,save_edit_location_survey_details,\
    save_edit_consumer_details
from v1.userapp.models.privilege import get_privilege_by_id
from api.messages import SUCCESS,STATE,ERROR,EXCEPTION,DATA

from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from v1.commonapp.views.pagination import StandardResultsSetPagination
from v1.survey.models.survey import Survey as SurveyTbl
from v1.survey.serializers.survey import SurveyViewSerializer



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
class SurveyListApiView(generics.ListAPIView):
    serializer_class = SurveyViewSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        search_str = self.request.query_params.get('search', None)

        queryset = Survey.objects.filter(is_active=True)
        utility_id_string = self.request.query_params.get('utility', None)
        category_id_string = self.request.query_params.get('category', None)
        sub_category_id_string = self.request.query_params.get('sub_category', None)
        area_id_string = self.request.query_params.get('area', None)
        sub_area_id_string = self.request.query_params.get('sub_area', None)
        type_id_string = self.request.query_params.get('type', None)
        objective_id_string = self.request.query_params.get('objective', None)
        status_id_string = self.request.query_params.get('status', None)

        if utility_id_string is not None:
            queryset = queryset.filter(utility__id_string=utility_id_string)
        if category_id_string is not None:
            category = get_consumer_category_by_id_string(category_id_string)
            queryset = queryset.filter(consumer_category_id=category.id)
        if sub_category_id_string is not None:
            sub_category = get_consumer_sub_category_by_id_string(sub_category_id_string)
            queryset = queryset.filter(sub_category_id=sub_category.id)
        if area_id_string is not None:
            area = get_area_by_id_string(area_id_string)
            queryset = queryset.filter(area_id=area.id)
        if sub_area_id_string is not None:
            sub_area = get_sub_area_by_id_string(sub_area_id_string)
            queryset = queryset.filter(sub_area_id=sub_area.id)
        if type_id_string is not  None:
            type = get_survey_type_by_id_string(type_id_string)
            queryset = queryset.filter(type_id=type.id)
        if objective_id_string is not  None:
            objective = get_survey_type_by_id_string(objective_id_string)
            queryset = queryset.filter(objective_id=objective.id)
        if status_id_string is not  None:
            status = get_survey_status_by_id_string(status_id_string)
            queryset = queryset.filter(status_id=status.id)

        if search_str is not None:
            queryset = Survey.objects.filter(is_active=True, name__icontains=search_str).order_by('-id')

        return queryset



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

class LocationSurveyApiView(GenericAPIView):
    def get(self, request,id_string):
        try:
            # Checking authentication start
            # if is_token_valid(request.data['token']):
            if is_token_valid(1):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                    # Checking authorization end

                    # Code for lookups start
                    # survey = get_survey_by_id_string(request.data['id_string'])
                    survey = get_survey_by_id_string(id_string=id_string)
                    area = get_area_by_id(survey.area_id)
                    sub_area = get_sub_area_by_id(survey.sub_area_id)
                    type = get_survey_type_by_id(survey.type_id)
                    objective = get_survey_type_by_id(survey.objective_id)
                    statususe = get_survey_status_by_id(survey.status_id)
                    consumer_category = get_consumer_category_by_id(survey.category_id)
                    sub_category = get_consumer_sub_category_by_id(survey.sub_category_id)

                    # Code for lookups end

                    # Code for sending Location Survey in response start
                    data = {
                        'tenant_id_string': survey.tenant.id_string,
                        'utility_id_string': survey.utility.id_string,
                        'name':survey.name,
                        'objective_id_string':objective.id_string,
                        'objective':objective.name,
                        'discription_id_string':survey.id_string,
                        'discription':survey.description,
                        'type_id_string':type.id_string,
                        'type':type.name,
                        'start_date': survey.start_date.strftime(DISPLAY_DATE_FORMAT),
                        'end_date': survey.end_date.strftime(DISPLAY_DATE_FORMAT),
                        'completion_date': survey.completion_date.strftime(DISPLAY_DATE_FORMAT),
                        'area_id_string': area.id_string,
                        'area': area.name,
                        'sub_area_id_string': sub_area.id_string,
                        'sub_area_name': sub_area.name,
                        'category_id_string':consumer_category.id_string,
                        'category':consumer_category.name,
                        'sub_category_id_string':sub_category.id_string,
                        'sub_category':sub_category.name,
                        'is_active': survey.is_active,
                        'status_id_string':statususe.id_string,
                        'status':statususe.status,
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
            # if is_token_valid(request.data['token']):
            if is_token_valid(1):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():

                    # Checking authorization end

                    # Request data verification start
                    user = UserDetail.objects.get(id=2)

                    if is_data_verified(request):
                        # Request data verification end

                        # check Survey is Already Exists or not
                        # if Survey.objects.get(name=request.data['survey_name'],area_id=request.data['area'],sub_area_id=request.data['sub_area'],\
                        #                     start_date=request.data['start_date'],end_date=request.data['end_date']).exists():
                        #
                        #     survey_data = {'survey_name':request.data['survey_name'],'area':request.data['area'],'sub_area':request.data['sub_area'],\
                        #                     'start_date':request.data['start_date'],'end_date':request.data['end_date']}
                        #
                        #     return Response({
                        #         STATE: ERROR,
                        #         'data': survey_data,
                        #     }, status=status.HTTP_409_CONFLICT)
                        #
                        # else:
                        # Save Location Survey start
                        sid = transaction.savepoint()
                        location_survey,result = save_survey_details(user,request,sid)
                        if result == False:
                            return Response({
                                STATE: EXCEPTION,
                                ERROR: ERROR
                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                            transaction.savepoint_commit(sid)
                            data = {
                                "Message": "Data Save Successfully !"
                            }
                            return Response({
                                STATE: SUCCESS,
                                DATA: data,
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
            if is_token_valid(1):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start

                    if is_data_verified(request):
                        # Request data verification end

                        # Update Location Survey start
                        user = UserDetail.objects.get(id=2)
                        location_survey,result = save_edit_location_survey_details(user,request)
                        if result == False:
                            return Response({
                                STATE: EXCEPTION,
                                ERROR: ERROR
                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                        # Update Location Survey start
                            data = {
                                "message":"update successfully !"
                            }

                            return Response({
                                STATE: SUCCESS,
                                DATA: data,
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
# API end Point: api/v1/consumer/
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

    def get(self, request,id_string):
        try:
            # Checking authentication start
            if is_token_valid(1):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                    # Checking authorization end

                    # if request.data['consumer_id_string']:

                    if SurveyConsumer.objects.get(id_string=id_string):
                        # Code for lookups start
                        consumer = get_survey_consumer_by_id_string(id_string=id_string)
                        area = get_area_by_id(consumer.area_id)
                        sub_area = get_sub_area_by_id(consumer.sub_area_id)
                        # statususe = get_survey_status_by_id(consumer.status_id)
                        # Code for lookups end

                        # Code for sending Consumer Survey in response start
                        data = {
                            'tenant_id_string': consumer.tenant.id_string,
                            'utility_id_string': consumer.utility.id_string,
                            'consumer_no':consumer.consumer_no,
                            'first_name':consumer.first_name,
                            'last_name':consumer.last_name,
                            'email_id':consumer.email_id,
                            'phone_mobile':consumer.phone_mobile,
                            'area_id_string': area.id_string,
                            'area': area.name,
                            'sub_area_id_string': sub_area.id_string,
                            'sub_area': sub_area.name,
                            'is_active': consumer.is_active,
                        }

                        return Response({
                            STATE: SUCCESS,
                            DATA: data,
                        }, status=status.HTTP_200_OK)
                        # Code for sending Consumer Survey in response end
                    else:
                        data = get_consumer_survey_list()
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
            if is_token_valid(1):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    if is_consumer_data_verified(request):
                        # Request data verification end

                        # check Survey is Already Exists or not
                        # if Survey.objects.get(name=request.data['survey_name'],area=request.data['area'],sub_area=request.data['sub_area'],
                        #                     start_date=request.data['start_date'],end_date=request.data['end_date']):
                        #
                        #     survey_data = {'survey_name':request.data['survey_name'],'area':request.data['area'],'sub_area':request.data['sub_area'],\
                        #                     'start_date':request.data['start_date'],'end_date':request.data['end_date']}
                        #
                        #     return Response({
                        #         STATE: ERROR,
                        #         'data': survey_data,
                        #     }, status=status.HTTP_409_CONFLICT)
                        #
                        # else:
                        survey_list = {}
                        # Save Consumer Survey start
                        sid = transaction.savepoint()
                        user = UserDetail.objects.get(id=2)
                        consumer_survey,result = save_survey_details(user,request,sid)
                        if result == False:
                            return Response({
                                STATE: EXCEPTION,
                                ERROR: ERROR
                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                        consumenr,result= save_consumer_details(request, user, consumer_survey)
                        survey_list['consumer_survey'] = consumer_survey
                        survey_list['consumer_details'] = result
                        if result == True:
                            transaction.savepoint_commit(sid)
                            data = {
                                "Message": "Data save successfully"
                            }
                        else:
                            data = {
                                "Message": "No Data save"
                            }
                        return Response({
                            STATE: SUCCESS,
                            DATA: data,
                        }, status=status.HTTP_200_OK)

                        # save all consumer details
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
            if is_token_valid(1):
                # payload = get_payload(request.data['token'])
                # user = get_user(payload['id_string'])
                # Checking authentication end

                # Checking authorization start
                # privilege = get_privilege_by_id(1)
                # sub_module = get_sub_module_by_id(1)
                if is_authorized():
                    # Checking authorization end

                    # Request data verification start
                    if is_consumer_data_verified(request):
                        # Request data verification end
                        survey_list = {}
                        # Update Consumer Survey start
                        user = UserDetail.objects.get(id=2)
                        if request.data['consumer_id_string']:
                            consumer_survey,result = save_edit_consumer_details(user,request)
                        else:
                            survey, result = save_edit_location_survey_details(user, request)

                        if result == False:
                            return Response({
                                STATE: EXCEPTION,
                                ERROR: ERROR
                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                            data = {
                                "message ": "Update Sucessfully !"
                            }
                            return Response({
                                STATE: SUCCESS,
                                DATA: data,
                            }, status=status.HTTP_200_OK)
                        # Update Consumer Survey start
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

