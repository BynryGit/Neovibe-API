__author__ = 'priyanka'

import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.campaign.models.campaign_group import CampaignGroup


class CampaignGroupTestCase(APITestCase):
    def get_all_campaign_group(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        utility_obj = UtilityMaster.objects.create(tenant=tenant_obj, name="utility_test")
        CampaignGroup.objects.create(tenant=tenant_obj,utility=utility_obj,name="campaign_group_1")
        response = self.client.get(reverse('campaign_group_list'))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # for getting single campaign details
    def get_single_campaign_group(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        group_obj = CampaignGroup.objects.create(tenant=tenant_obj, name="campaign_group_2")
        response = self.client.get(reverse('campaign_group_detail', args=[group_obj.id_string]))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
