from django.contrib import admin
from v1.campaign.models.ad_assignment_status import AdAssignStatus
from v1.campaign.models.advert_assign import AdvertisementAssignment
from v1.campaign.models.advert_status import AdvertStatus
from v1.campaign.models.advertisement import Advertisements
from v1.campaign.models.advertisement_type import AdvertisementType
from v1.campaign.models.campaign import Campaign
from v1.campaign.models.campaign_group import CampaignGroup
from v1.campaign.models.campaign_objective import CampaignObjective
from v1.campaign.models.campaign_type import CampaignType
from v1.campaign.models.campaign_subtype import CampaignSubType
from v1.campaign.models.advertisement_subtype import AdvertisementSubType


admin.site.register(AdAssignStatus)
admin.site.register(AdvertisementAssignment)
admin.site.register(AdvertStatus)
admin.site.register(Advertisements)
admin.site.register(AdvertisementType)
admin.site.register(AdvertisementSubType)
admin.site.register(Campaign)
admin.site.register(CampaignGroup)
admin.site.register(CampaignObjective)
admin.site.register(CampaignType)
admin.site.register(CampaignSubType)
