import traceback

from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from api.messages import *
from v1.commonapp.models.department import get_department_by_tenant_id_string, get_department_by_id_string
from v1.commonapp.serializers.department import DepartmentListSerializer, DepartmentViewSerializer
from v1.commonapp.views.pagination import StandardResultsSetPagination

# API Header
# API end Point: api/v1/department/list
# API verb: GET
# Package: Basic
# Modules: Lookup
# Sub Module: Lookup
# Interaction: View Departments
# Usage: This will get the list of departments
# Tables used: Lookup - 2.12.16 Lookup - Department
# Author: Arpita
# Created on: 06/05/2020
# Updated on: 12/05/2020


class DepartmentList(generics.ListAPIView):
    serializer_class = DepartmentListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        queryset = get_department_by_tenant_id_string(1)
        utility_id_string = self.request.query_params.get('utility', None)

        if utility_id_string is not None:
            queryset = queryset.filter(utility__id_string=utility_id_string)
        return queryset


# API Header
# API end Point: api/v1/department
# API verb: GET
# Package: Basic
# Modules: Lookup
# Sub Module: Lookup
# Interaction: View Department
# Usage: This will get the detail of department
# Tables used: Lookup - 2.12.16 Lookup - Department
# Author: Arpita
# Created on: 12/05/2020


class Department(GenericAPIView):

    def get(self, request, id_string):
        try:
            department = get_department_by_id_string(id_string)
            if department:
                serializer = DepartmentViewSerializer(instance=department, context={'request': request})
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