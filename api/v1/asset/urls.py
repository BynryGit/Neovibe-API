from django.urls import path
from v1.asset.views.asset import AssetList,AssetDetail,Asset

urlpatterns = [
    path('list', AssetList.as_view(), name="asset_list"),
    path('', Asset.as_view(), name="asset"),
    path('<uuid:id_string>', AssetDetail.as_view(), name="asset_detail"),
]

