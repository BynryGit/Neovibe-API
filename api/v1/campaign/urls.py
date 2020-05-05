from django.urls import path
from v1.campaign.views.campaigns import CampaignListApiView

urlpatterns = [
    path('list/', CampaignListApiView.as_view())
]