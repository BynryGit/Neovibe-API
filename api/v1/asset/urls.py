from django.urls import path
from v1.asset.views.asset import AssetList,AssetDetail,Asset
from v1.asset.views.asset_status import AssetstatusList,AssetStatusDetail
from v1.asset.views.category import AssetCategoryList,AssetCategoryDetail
from v1.asset.views.sub_category import AssetSubCategoryList,AssetSubCategoryDetail
from v1.dispatcher.views.sop import SOPList,SOPDetail
from v1.dispatcher.views.service_request import ServiceRequest,ServiceRequestDetail
from v1.dispatcher.views.service_assignment import ServiceAssignment,ServiceAssignmentDetail
from v1.asset.views.history import ServiceHistoryList,ServiceHistoryDetail
from v1.asset.views.resources import ResourceList,ResourceDetail

urlpatterns = [
    path('list', AssetList.as_view(), name="asset_list"),
    path('', Asset.as_view(), name="asset"),
    path('<uuid:id_string>', AssetDetail.as_view(), name="asset_detail"),

    path('status/list', AssetstatusList.as_view(), name="asset_status_list"),
    path('status/<uuid:id_string>', AssetStatusDetail.as_view(), name="asset_status_detail"),

    path('category/list', AssetCategoryList.as_view(), name="asset_category_list"),
    path('category/<uuid:id_string>', AssetCategoryDetail.as_view(), name="asset_category_detail"),

    path('sub_category/list', AssetSubCategoryList.as_view(), name="asset_sub_category_list"),
    path('sub_category/<uuid:id_string>', AssetSubCategoryDetail.as_view(), name="asset_sub_category_detail"),

    path('sop/list', SOPList.as_view(), name="sop_list"),
    path('sop/<uuid:id_string>', SOPDetail.as_view(), name="sop_detail"),

    path('<uuid:id_string>/service-request', ServiceRequest.as_view(), name="service_request"),
    path('service-request/<uuid:id_string>', ServiceRequestDetail.as_view(), name="service_request_detail"),

    path('<uuid:id_string>/service-assign', ServiceAssignment.as_view(), name="service_assign"),
    path('service-assign/<uuid:id_string>', ServiceAssignmentDetail.as_view(), name="service_assign_detail"),

    path('<uuid:id_string>/history/list', ServiceHistoryList.as_view(), name="service_history_list"),
    path('history/<uuid:id_string>', ServiceHistoryDetail.as_view(), name="service_history_detail"),

    path('resource/list', ResourceList.as_view(), name="resource_list"),
    path('resource/<uuid:id_string>', ResourceDetail.as_view(), name="resource_detail"),


]

