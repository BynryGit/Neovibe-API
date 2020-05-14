from django.urls import path
from v1.campaign.views.campaigns import CampaignList,Campaigns
from v1.campaign.views.advertisement import Advertisment,AdvertismentList
from v1.campaign.views.campaign_group import CampaignGroupList,CampaignGroupView
from v1.campaign.views.campaign_objective import CampaignObjectiveList,CampaignObjectiveView
from v1.campaign.views.campaign_status import CampaignstatusList,CampaignStatusView
from v1.campaign.views.advertisement_type import AdvertisementTypeList,AdvertisementTypeView
from v1.campaign.views.advertisement_status import AdvertisementStatusList,AdvertisementStatusView


urlpatterns = [
    path('', CampaignList.as_view(), name="campaign_list"),
    path('<uuid:id_string>/', Campaigns.as_view(),name="campaign_data"),
    path('advert/<uuid:id_string>/', Advertisment.as_view(),name="advertisement_data"),
    path('<uuid:id_string>/adverts/', AdvertismentList.as_view(),name="advertisement_list"),
    path('group/list', CampaignGroupList.as_view(),name="campaign_gropu_list"),
    path('group/<uuid:id_string>/', CampaignGroupView.as_view(),name="campaign_group"),
    path('objective/list', CampaignObjectiveList.as_view(),name="campaign_objective_list"),
    path('objective/<uuid:id_string>/', CampaignObjectiveView.as_view(),name="campaign_objective"),
    path('campaign-status/list/', CampaignstatusList.as_view(), name="campaign_status_list"),
    path('status/<uuid:id_string>/', CampaignStatusView.as_view(), name="campaign_status"),
    path('advert-type/list/', AdvertisementTypeList.as_view(), name="advert_type_list"),
    path('advert-type/<uuid:id_string>/', AdvertisementTypeView.as_view(), name="advert_type"),
    path('advert-status/list', AdvertisementStatusList.as_view(), name="advert_status_list"),
    path('advert-status/<uuid:id_string>/', AdvertisementStatusView.as_view(), name="advert_status"),
]

