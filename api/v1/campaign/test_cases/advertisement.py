__author__ = 'priyanka'

import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.campaign.models.advertisement import Advertisements
from v1.campaign.models.campaign import Campaign


class AdvertisementTestCase(APITestCase):
    def get_all_advertisement(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        utility_obj = UtilityMaster.objects.create(tenant=tenant_obj, name="utility_test")
        campaign = Campaign.objects.create(tenant=tenant_obj, name="Testing TDD")
        Advertisements.objects.create(tenant=tenant_obj,campaign_id=campaign.id,utility=utility_obj,name="Smart360-Awareness-Gas")
        response = self.client.get(reverse('advertisement_list',args=[campaign.id_string]))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_single_advertisement(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        advertisements = Advertisements.objects.create(tenant=tenant_obj, name="Smart360-Awareness-Power")
        response = self.client.get(reverse('advertisement_data', args=[advertisements.id_string]))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
