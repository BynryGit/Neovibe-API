__author__ = 'aki'

# TestCase header
# module: Utility
# Test case : API testing
# Test Case description :
# Black box testing for utility APIs for
# 1. utility list - Total pages, Next and back operations, Filter, Search, Multiple Utility
# 2. Add utility: Create utility, success message, fail message
# 3. View utility: Get valid data against single utility
# 4. Edit utility: Get valid data, update valid and invalid data, duplicate records
# # reference tables : registration master, payments, documents, notes
# author : Gauri Deshmukh Nibrad
# created on : 29/04/2020

# change history
# <ddmmyyyy><changes><author>

import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


class UtilityTestCase(APITestCase):

    # dummy data to save in test database
    def setUp(self):
        self.valid_payload = {
            "tenant": "1",
            "short_name": "MNGL",
            "name": "MNGL-RAJURA",
            "phone_no": "1111111111",
            "email_id": "abc@gmail.com"
        }
        self.invalid_payload = {
            "tenant": "",
            "short_name": "MNGL",
            "name": "MNGL-RAJURA",
            "phone_no": "1111111111",
            "email_id": "abc@gmail.com"
        }

        self.update_payload = {
            "tenant": "1",
            "short_name": "MNGL",
            "name": "MNGL-Chandrapur",
        }

    # for save valid utility details
    def create_valid_utility(self):
        response = self.client.post("api/v1/utilities/", self.valid_payload)
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # for save invalid utility details and through error
    def create_invalid_utility(self):
        response = self.client.post("api/v1/utilities/", self.invalid_payload)
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # for getting all registration list by search, filter, and total records
    def get_all_utilities(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        UtilityMaster.objects.create(tenant=tenant_obj, name="utility_test")
        response = self.client.get(reverse('utility_list'))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # for getting single utility details
    def get_single_utility(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        utility_obj = UtilityMaster.objects.create(tenant=tenant_obj, name="utility_test")
        response = self.client.get(reverse('utility_detail', args=[utility_obj.id_string]))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # for update single utility record
    def update_valid_utility(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        utility_obj = UtilityMaster.objects.create(tenant=tenant_obj, name="utility_test")
        response = self.client.put(reverse('utility_detail', args=[utility_obj.id_string]), self.update_payload)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# you can print API response in folowing three different ways.
# print("response",response.content)
# print("response data", response.data)
# print("response json",json.loads(response.content))