from django.urls import path
from v1.asset.views.asset import AssetList,AssetDetail,Asset
from v1.asset.views.asset_status import AssetstatusList,AssetStatusDetail
from v1.asset.views.category import AssetCategoryList,AssetCategoryDetail
from v1.asset.views.sub_category import AssetSubCategoryList,AssetSubCategoryDetail
from v1.dispatcher.views.sop import SOPList,SOPDetail

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
]

