from django.urls import path
from v1.work_order.views.work_order_rules import WorkOrderRuleList
from v1.work_order.views.work_order_master import WorkOrderMasterList,WorkOrderService,WorkOrderDetail


urlpatterns = [
    path('utility/<uuid:id_string>/rules/list', WorkOrderRuleList.as_view(), name='work_order_rules_list'),
    path('utility/<uuid:id_string>/service/list', WorkOrderMasterList.as_view(), name='work_order_master_list'),
    path('utility/service', WorkOrderService.as_view(), name='work_order_service'),
    path('utility/service/<uuid:id_string>', WorkOrderDetail.as_view(), name='work_order_service_detail'),
]