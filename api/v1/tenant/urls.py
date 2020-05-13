__author__ = "Gauri"

from django.urls import path

from v1.tenant.views.tenant import TenantListDetail,TenantDetail
# UtilityListDetail, UtilityDetail


urlpatterns = [
    path('', TenantListDetail.as_view(), name='tenant_list'),
    path('<uuid:id_string>/', TenantDetail.as_view(),name='tenant_detail'),
]