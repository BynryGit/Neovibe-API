__author__ = 'priyanka'

import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.campaign.models.campaign_objective import CampaignObjective


class CampaignObjectiveTestCase(APITestCase):
    def get_all_campaign_objective(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        utility_obj = UtilityMaster.objects.create(tenant=tenant_obj, name="utility_test")
        CampaignObjective.objects.create(tenant=tenant_obj,utility=utility_obj,name="awareness")
        response = self.client.get(reverse('campaign_objective_list'))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # for getting single campaign details
    def get_single_campaign_objective(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        objective_obj = CampaignObjective.objects.create(tenant=tenant_obj, name="brand awareness")
        response = self.client.get(reverse('campaign_objective_detail', args=[objective_obj.id_string]))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
