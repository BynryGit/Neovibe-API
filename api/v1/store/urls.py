from django.urls import path
from v1.store.views.store_type import StoreTypeList, StoreTypeDetail, StoreType
from v1.store.views.store_location import StoreLocationList, StoreLocationDetail, StoreLocation

urlpatterns = [

    path('<uuid:id_string>/type/list', StoreTypeList.as_view(), name='store_type_list'),
    path('<uuid:id_string>/type', StoreTypeDetail.as_view(), name='store_type_detail'),
    path('type', StoreType.as_view(), name='store_type'),

    path('<uuid:id_string>/location/list', StoreLocationList.as_view(), name='store_location_list'),
    path('<uuid:id_string>/location', StoreLocationDetail.as_view(), name='store_location_detail'),
    path('location', StoreLocation.as_view(), name='store_location'),




]