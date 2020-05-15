__author__ = 'priyanka'

import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.campaign.models.campaign_status import CampaignStatus


class CampaignStatusTestCase(APITestCase):
    def get_all_campaign_status(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        utility_obj = UtilityMaster.objects.create(tenant=tenant_obj, name="utility_test")
        CampaignStatus.objects.create(tenant=tenant_obj,utility=utility_obj,name="Hold")
        response = self.client.get(reverse('campaign_status_list'))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # for getting single campaign details
    def get_single_campaign_status(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        status_obj = CampaignStatus.objects.create(tenant=tenant_obj, name="Created")
        response = self.client.get(reverse('campaign_status', args=[status_obj.id_string]))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
