from django.urls import path
from v1.campaign.views.campaigns import CampaignListApiView,CampaignApiView

urlpatterns = [
    path('<uuid:id_string>/', CampaignApiView.as_view(),name="campaign_data"),
    path('list/', CampaignListApiView.as_view(),name="campaign_list")
]