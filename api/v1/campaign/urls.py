from django.urls import path
from v1.campaign.views.campaigns import CampaignListApiView,CampaignApiView

urlpatterns = [
    path('', CampaignApiView.as_view()),
    path('list/', CampaignListApiView.as_view())
]