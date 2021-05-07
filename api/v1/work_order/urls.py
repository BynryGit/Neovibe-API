from django.urls import path
from v1.work_order.views.work_order_rules import WorkOrderRuleList
from v1.work_order.views.work_order_master import WorkOrderMasterList,WorkOrderService,WorkOrderDetail
from v1.work_order.views.service_appointment import ServiceAppointment,ServiceAppointmentList,ServiceAppointmentDetail, ServiceAppointmentLifeCycleList, ServiceAppointmentReject, ServiceAppointmentHold, ServiceAppointmentApprove
from v1.work_order.views.material_type import MaterialTypeList
from v1.work_order.views.material_subtype import MaterialSubTypeList
from v1.work_order.views.material_name import MaterialNameList
from v1.work_order.views.service_assignment import ServiceAssignment,ServiceDessignmentDetail,ServiceAssignmentDetail,ServiceAssignmentList
from v1.work_order.views.scheduled_appointment import ScheduledAppointment

urlpatterns = [
    path('utility/<uuid:id_string>/rules/list', WorkOrderRuleList.as_view(), name='work_order_rules_list'),
    path('utility/<uuid:id_string>/list', WorkOrderMasterList.as_view(), name='work_order_master_list'),
    path('utility/service', WorkOrderService.as_view(), name='work_order_service'),
    path('utility/service/<uuid:id_string>', WorkOrderDetail.as_view(), name='work_order_service_detail'),
    path('service-appointment', ServiceAppointment.as_view(), name='service_appointment'),
    # path('utility/<uuid:id_string>/service-appointment/list',ServiceAppointmentList.as_view(),name='service_appointment_list'),
    path('utility/<uuid:id_string>/material_type/list', MaterialTypeList.as_view(), name='material_type_list'),
    path('utility/<uuid:id_string>/material_subtype/list', MaterialSubTypeList.as_view(), name='material_subtype_list'),
    path('utility/<uuid:id_string>/material_name/list', MaterialNameList.as_view(), name='material_name_list'),
    path('service-appointment/<uuid:id_string>',ServiceAppointmentDetail.as_view(),name="service_appointment_detail"),
    path('service-assignment',ServiceAssignment.as_view(),name="service_assignment"),
    path('service-deassignment/<uuid:id_string>',ServiceDessignmentDetail.as_view(),name="service_deassignment"),
    path('service-assignment/<uuid:id_string>',ServiceAssignmentDetail.as_view(),name="service_assignment_detail"),
    path('utility/<uuid:utility_id_string>/user/<uuid:user_id_string>/service-assignment/list',ServiceAssignmentList.as_view(),name="service_assignment_list"),
    path('scheduled-appointment',ScheduledAppointment.as_view(), name="add_scheduled_appointment"),
    path('service-appointment/<uuid:id_string>/life-cycle',ServiceAppointmentLifeCycleList.as_view(),name="service_life_cycle"),
    # path('service-appointment/<uuid:id_string>/disconnect-list',ServiceAppointmentConsumerDisconnectList.as_view(), name="service_disconnect_list"),
    path('service-appointment/<uuid:id_string>/list',ServiceAppointmentList.as_view(),name='service_appointment_list'),
    path('service-appointment/list',ServiceAppointmentList.as_view(),name='service_appointment_list'),
    path('service-appointment/<uuid:id_string>/reject',ServiceAppointmentReject.as_view(),name='service_appointment_reject'),
    path('service-appointment/<uuid:id_string>/hold',ServiceAppointmentHold.as_view(),name='service_appointment_hold'),
    path('service-appointment/<uuid:id_string>/approve',ServiceAppointmentApprove.as_view(),name='service_appointment_approve'),

]