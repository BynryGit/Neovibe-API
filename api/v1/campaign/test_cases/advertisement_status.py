__author__ = 'priyanka'

import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.campaign.models.advert_status import AdvertStatus


class AdvertStatusTestCase(APITestCase):
    def get_all_advertisement_status(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        utility_obj = UtilityMaster.objects.create(tenant=tenant_obj, name="utility_test")
        AdvertStatus.objects.create(tenant=tenant_obj,utility=utility_obj,name="created")
        response = self.client.get(reverse('advert_status_list'))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_single_advertisement_status(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        advert_type = AdvertStatus.objects.create(tenant=tenant_obj, name="Assigned")
        response = self.client.get(reverse('advert_status_detail', args=[advert_type.id_string]))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
