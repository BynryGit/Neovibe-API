__author__ = 'priyanka'

import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.userapp.models.user_master import UserDetail
from v1.campaign.models.campaign import Campaign




class CampaignTestCase(APITestCase):

    # dummy data to save in test database
    def setUp(self):
        self.valid_payload = {
            "tenant":4,
            "campaign_name":"Smart360 UnitTesting",
            "start_date":"2020-06-13",
            "end_date":"2020-07-10",
            "description":"This is for UnitTesting of POST Method ",
            "frequency_id_string":"1874cf50-c3d7-478f-b6c3-5814062f1873",
            "potential_consumers":500,
            "actual_consumers":400,
            "budget_amount":1000,
            "actual_amount":500,

        }
        self.invalid_payload = {
            "tenant": "",
            "campaign_name":"Smart360 UnitTesting",
            "start_date":"2020-06-13",
            "end_date":"2020-07-10",
            "description":"This is for UnitTesting of POST Method ",
            "frequency_id_string":"",
        }

        self.update_payload = {
            "tenant": "1",
            "campaign_name":"Smart360 UnitTesting",
            "start_date":"2021-01-01",
            "end_date":"2021-02-01",
        }

    # for save valid campaign details
    def create_valid_campaign(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        UserDetail.objects.create(tenant=tenant_obj,user_type=1, user_subtype=1, form_factor_id=1, user_name="Testing")
        response = self.client.post("api/v1/campaign/", self.valid_payload)
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # for save invalid campaign details and through error
    def create_invalid_campaign(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        UserDetail.objects.create(tenant=tenant_obj,user_type=1, user_subtype=1,form_factor_id=1,user_name="Testing")
        response = self.client.post("api/v1/campaign/", self.invalid_payload)
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # for getting all campaign list by search, filter, and total records
    def get_all_campaign(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        UserDetail.objects.create(tenant=tenant_obj,user_type=1,user_subtype=1,form_factor_id=1,user_name="Testing")
        response = self.client.get(reverse('campaign_list'))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # for getting single campaign details
    def get_single_campaign(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        campaign_obj = Campaign.objects.create(tenant=tenant_obj)
        response = self.client.get(reverse('campaign_data', args=[campaign_obj.id_string]))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # for update single campaign record
    def update_valid_campaign(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        campaign_obj = Campaign.objects.create(tenant=tenant_obj)
        response = self.client.put(reverse('campaign_data', args=[campaign_obj.id_string]), self.update_payload)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# you can print API response in foloowing three different ways.
# print("response",response.content)
# print("response data", response.data)
# print("response json",json.loads(response.content))