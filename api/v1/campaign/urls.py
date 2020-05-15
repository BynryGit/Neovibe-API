from django.urls import path
from v1.campaign.views.campaigns import CampaignList,CampaignDetail,Campaign
from v1.campaign.views.advertisement import AdvertismentDetail,AdvertismentList
from v1.campaign.views.campaign_group import CampaignGroupList,CampaignGroupDetail
from v1.campaign.views.campaign_objective import CampaignObjectiveList,CampaignObjectiveDetail
from v1.campaign.views.campaign_status import CampaignstatusList,CampaignStatusDetail
from v1.campaign.views.advertisement_type import AdvertisementTypeList,AdvertisementTypeDetail
from v1.campaign.views.advertisement_status import AdvertisementStatusList,AdvertisementStatusDetail


urlpatterns = [
    path('', Campaign.as_view(), name="campaign"),
    path('list', CampaignList.as_view(), name="campaign_list"),
    path('<uuid:id_string>/', CampaignDetail.as_view(),name="campaign_detail"),
    path('advert/<uuid:id_string>/', AdvertismentDetail.as_view(),name="advertisement_detail"),
    path('<uuid:id_string>/adverts/', AdvertismentList.as_view(),name="advertisement_list"),
    path('group/list', CampaignGroupList.as_view(),name="campaign_group_list"),
    path('group/<uuid:id_string>/', CampaignGroupDetail.as_view(),name="campaign_group_detail"),
    path('objective/list', CampaignObjectiveList.as_view(),name="campaign_objective_list"),
    path('objective/<uuid:id_string>/', CampaignObjectiveDetail.as_view(),name="campaign_objective_detail"),
    path('campaign-status/list/', CampaignstatusList.as_view(), name="campaign_status_list"),
    path('status/<uuid:id_string>/', CampaignStatusDetail.as_view(), name="campaign_status_detail"),
    path('advert-type/list/', AdvertisementTypeList.as_view(), name="advert_type_list"),
    path('advert-type/<uuid:id_string>/', AdvertisementTypeDetail.as_view(), name="advert_type_detail"),
    path('advert-status/list', AdvertisementStatusList.as_view(), name="advert_status_list"),
    path('advert-status/<uuid:id_string>/', AdvertisementStatusDetail.as_view(), name="advert_status_detail"),
]

