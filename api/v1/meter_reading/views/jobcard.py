# __author__ = "aki"
#
# import traceback
# from rest_framework.generics import GenericAPIView
# from rest_framework import status
# from rest_framework.response import Response
# from api.messages import SUCCESS, STATE, ERROR, EXCEPTION, DUPLICATE, RESULT, DATA_ALREADY_EXISTS
# from master.models import User
# from v1.commonapp.common_functions import is_token_valid, is_authorized
# from v1.commonapp.views.logger import logger
# from v1.meter_reading.models.route import get_route_by_id_string
# from v1.meter_reading.serializers.jobcard import JobcardSerializer, JobcardViewSerializer
# from v1.supplier.serializers.supplier_invoice import SupplierInvoiceViewSerializer, SupplierInvoiceSerializer
#
#
# # API Header
# # API end Point: api/v1/route/id_string/assign
# # API verb: POST
# # Package: Basic
# # Modules: Meter Data
# # Sub Module:
# # Interaction: Create job card according route
# # Usage: API will create job card object based on valid data
# # Tables used: 2.3.8.3 Jobcard
# # Author: Akshay
# # Created on: 15/06/2020
#
# class AssignRoute(GenericAPIView):
#     serializer_class = JobcardSerializer
#
#     def post(self, request, id_string):
#         try:
#             # Checking authentication start
#             if is_token_valid(request.headers['token']):
#                 # payload = get_payload(request.headers['token'])
#                 # user = get_user(payload['id_string'])
#                 # Checking authentication end
#
#                 # Checking authorization start
#                 if is_authorized():
#                 # Checking authorization end
#                     # Todo fetch user from request start
#                     user = User.objects.get(id=2)
#                     # Todo fetch user from request end
#                     route_obj = get_route_by_id_string(id_string)
#                     if route_obj:
#                         serializer = JobcardSerializer(data=request.data)
#                         if serializer.is_valid():
#                             jobcard_obj = serializer.create(serializer.validated_data, route_obj, user)
#                             if jobcard_obj:
#                                 serializer = JobcardViewSerializer(jobcard_obj, context={'request': request})
#                                 return Response({
#                                     STATE: SUCCESS,
#                                     RESULT: serializer.data,
#                                 }, status=status.HTTP_201_CREATED)
#                             else:
#                                 return Response({
#                                     STATE: DUPLICATE,
#                                     RESULT: DATA_ALREADY_EXISTS,
#                                 }, status=status.HTTP_409_CONFLICT)
#                         else:
#                             return Response({
#                                 STATE: ERROR,
#                                 RESULT: serializer.errors,
#                             }, status=status.HTTP_400_BAD_REQUEST)
#                     else:
#                         return Response({
#                             STATE: ERROR,
#                         }, status=status.HTTP_404_NOT_FOUND)
#                 else:
#                     return Response({
#                         STATE: ERROR,
#                     }, status=status.HTTP_403_FORBIDDEN)
#             else:
#                 return Response({
#                     STATE: ERROR,
#                 }, status=status.HTTP_401_UNAUTHORIZED)
#         except Exception as ex:
#             logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
#             return Response({
#                 STATE: EXCEPTION,
#                 ERROR: str(traceback.print_exc(ex))
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#
# # API Header
# # API end Point: api/v1/supplier/invoice/id_string
# # API verb: GET, PUT
# # Package: Basic
# # Modules: Supplier
# # Sub Module: Invoice
# # Interaction: For edit and get single supplier invoice
# # Usage: API will edit and get supplier invoice
# # Tables used: 2.5.9 Supplier Invoice
# # Author: Akshay
# # Created on: 21/05/2020
#
# class SupplierInvoiceDetail(GenericAPIView):
#     serializer_class = SupplierInvoiceSerializer
#
#     def put(self, request, id_string):
#         try:
#             # Checking authentication start
#             if is_token_valid(request.headers['token']):
#                 # payload = get_payload(request.headers['token'])
#                 # user = get_user(payload['id_string'])
#                 # Checking authentication end
#
#                 # Checking authorization start
#                 if is_authorized():
#                 # Checking authorization end
#                     # Todo fetch user from request start
#                     user = User.objects.get(id=2)
#                     # Todo fetch user from request end
#
#                     supplier_invoice_obj = get_supplier_invoice_by_id_string(id_string)
#                     if supplier_invoice_obj:
#                         serializer = SupplierInvoiceSerializer(data=request.data)
#                         if serializer.is_valid():
#                             supplier_invoice_obj = serializer.update(supplier_invoice_obj, serializer.validated_data, user)
#                             serializer = SupplierInvoiceViewSerializer(supplier_invoice_obj, context={'request': request})
#                             return Response({
#                                 STATE: SUCCESS,
#                                 RESULT: serializer.data,
#                             }, status=status.HTTP_200_OK)
#                         else:
#                             return Response({
#                                 STATE: ERROR,
#                                 RESULT: serializer.errors,
#                             }, status=status.HTTP_400_BAD_REQUEST)
#                     else:
#                         return Response({
#                             STATE: ERROR,
#                         }, status=status.HTTP_404_NOT_FOUND)
#                 else:
#                     return Response({
#                         STATE: ERROR,
#                     }, status=status.HTTP_403_FORBIDDEN)
#             else:
#                 return Response({
#                     STATE: ERROR,
#                 }, status=status.HTTP_401_UNAUTHORIZED)
#         except Exception as ex:
#             logger().log(ex, 'ERROR', user=request.user, name=request.user.username)
#             return Response({
#                 STATE: EXCEPTION,
#                 ERROR: str(traceback.print_exc(ex))
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)