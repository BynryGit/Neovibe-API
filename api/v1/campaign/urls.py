from django.urls import path
from v1.campaign.views.campaigns import CampaignList,CampaignDetail,Campaign
from v1.campaign.views.advertisement import AdvertismentDetail,AdvertismentList,Advertisement
from v1.campaign.views.campaign_group import CampaignGroupList,CampaignGroupDetail
from v1.campaign.views.campaign_objective import CampaignObjectiveList,CampaignObjectiveDetail
from v1.campaign.views.campaign_status import CampaignstatusList,CampaignStatusDetail
from v1.campaign.views.advertisement_type import AdvertisementTypeList,AdvertisementTypeDetail,AdvertisementType
from v1.campaign.views.advertisement_subtype import AdvertisementSubTypeList,AdvertisementSubTypeDetail,AdvertisementSubType
from v1.campaign.views.advertisement_status import AdvertisementStatusList,AdvertisementStatusDetail
from v1.campaign.views.campaign_type import CampaignTypeList,CampaignType,CampaignTypeDetail
from v1.campaign.views.campaign_subtype import CampaignSubTypeList,CampaignSubType,CampaignSubTypeDetail

urlpatterns = [
    path('list', CampaignList.as_view(), name="campaign_list"),
    path('', Campaign.as_view(), name="campaign"),
    path('<uuid:id_string>', CampaignDetail.as_view(),name="campaign_detail"),

    path('utility/<uuid:id_string>/advert_type/list', AdvertisementTypeList.as_view(),name="advertisement_type_list"),
    path('advert_type/<uuid:id_string>', AdvertisementTypeDetail.as_view(),name="advertisement_type_detail"),
    path('advert_type', AdvertisementType.as_view(),name="advertisement_type"),
    path('utility/<uuid:id_string>/advert_subtype/list', AdvertisementSubTypeList.as_view(),name="advertisement_subtype_list"),
    path('advert_subtype/<uuid:id_string>', AdvertisementSubTypeDetail.as_view(),name="advertisement_subtype_detail"),
    path('advert_subtype', AdvertisementSubType.as_view(),name="advertisement_subtype"),

    path('group/list', CampaignGroupList.as_view(),name="campaign_group_list"),
    path('group/<uuid:id_string>', CampaignGroupDetail.as_view(),name="campaign_group_detail"),

    path('objective/list', CampaignObjectiveList.as_view(),name="campaign_objective_list"),
    path('objective/<uuid:id_string>', CampaignObjectiveDetail.as_view(),name="campaign_objective_detail"),

    path('campaign-status/list', CampaignstatusList.as_view(), name="campaign_status_list"),
    path('campaign-status/<uuid:id_string>', CampaignStatusDetail.as_view(), name="campaign_status_detail"),

    path('advert-type/list', AdvertisementTypeList.as_view(), name="advert_type_list"),
    path('advert-type/<uuid:id_string>', AdvertisementTypeDetail.as_view(), name="advert_type_detail"),

    path('advert-status/list', AdvertisementStatusList.as_view(), name="advert_status_list"),
    path('advert-status/<uuid:id_string>', AdvertisementStatusDetail.as_view(), name="advert_status_detail"),
    path('utility/<uuid:id_string>/campaign_type/list', CampaignTypeList.as_view(), name="campaign_type_list"),
    path('campaign_type/<uuid:id_string>', CampaignTypeDetail.as_view(), name="campaign_type_detail"),
    path('campaign_type', CampaignType.as_view(), name="campaign_type"),
    path('utility/<uuid:id_string>/campaign_subtype/list', CampaignSubTypeList.as_view(), name="campaign_subtype_list"),
    path('campaign_subtype/<uuid:id_string>', CampaignSubTypeDetail.as_view(), name="campaign_subtype_detail"),
    path('campaign_subtype', CampaignSubType.as_view(), name="campaign_subtype")
]

