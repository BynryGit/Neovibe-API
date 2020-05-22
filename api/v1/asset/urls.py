from django.urls import path
from v1.asset.views.asset import AssetList,AssetDetail,Asset
from v1.asset.views.asset_status import AssetstatusList,AssetStatusDetail

urlpatterns = [
    path('list', AssetList.as_view(), name="asset_list"),
    path('', Asset.as_view(), name="asset"),
    path('<uuid:id_string>', AssetDetail.as_view(), name="asset_detail"),

    path('status-list', AssetstatusList.as_view(), name="asset_status_list"),
    path('status/<uuid:id_string>', AssetStatusDetail.as_view(), name="asset_status_detail"),
]

