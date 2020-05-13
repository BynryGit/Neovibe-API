from django.urls import path
from v1.campaign.views.campaigns import CampaignList,Campaigns
from v1.campaign.views.advertisement import Advertisment,AdvertismentList

urlpatterns = [
    path('', CampaignList.as_view(), name="campaign_list"),
    path('<uuid:id_string>/', Campaigns.as_view(),name="campaign_data"),
    path('advert/<uuid:id_string>/', Advertisment.as_view(),name="advertisement_data"),
    path('<uuid:id_string>/adverts/', AdvertismentList.as_view(),name="advertisement_list"),
]