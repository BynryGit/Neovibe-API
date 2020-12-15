__author__ = 'aki'
# TestCase header
# module: S&M, Consumer care &Ops | sub-module - Registration
# Test case : API testing
# Test Case description :
# Black box testing for registration APIs for
# 1. Registration list - Total pages, Next and back operations, Filter, Search, Single Utility, Multiple Utility (Valid and Invalid data)
# 2. Add registration: Create registration, success message, fail message, duplicate entry, Payment entry, Documents entry, Notes entry, Valid and invalid data
# 3. View registration: Get valid data, payment, documents, Notes, Address, status, valid and invalid data
# 4. Edit registration: Get valid data, update valid and invalid data, duplicate records
# # reference tables : registration master, payments, documents, notes
# author : Gauri Deshmukh Nirbad
# created on : 29/04/2020

# change history
# <ddmmyyyy><changes><author>


import json
from django.test import TestCase, Client, client
from django.urls import reverse
from rest_framework import status


class RegistrationTestCase(TestCase):
    # initialize the APIClient app
    client = Client()

    def setUp(self):
        self.valid_payload = {
            "registration_no": "NSC10000001",
            "first_name": "first",
            "middle_name": "middle",
            "last_name": "last",
            "email_id": "gail@gmail.com",
            "phone_mobile": "7020929071",
            "phone_landline": "2571524",
            "address_line_1": "2571524",
            "street": "2571524",
            "zipcode": 456342,
            "region_id": 3,
            "country_id": 3,
            "state_id": 1,
            "city_id": 1,
            "area_id": 1,
            "sub_area_id": 1,
            "scheme_id": 1,
            "payment_id": 5,
            "ownership_id": 1,
            "consumer_category_id": 1,
            "sub_category_id": 1,
            "is_vip": True,
            "connectivity": True,
            "registration_channel_id": 1,
            "source_id": 1,
            "registration_date": "30-04-2020",
            "is_active": True,
            "created_by": True,
            "updated_by": True,
            "created_date": True,
            "updated_date": True
        }
        self.invalid_payload = {
            "registration_no": "",
            "first_name": "",
            "middle_name": "",
            "last_name": "",
            "email_id": "gail@gmail.com",
            "phone_mobile": "7020929071",
            "phone_landline": "2571524",
            "address_line_1": "2571524",
            "street": "2571524",
            "zipcode": 456342,
            "region_id": 3,
            "country_id": 3,
            "state_id": 1,
            "city_id": 1,
            "area_id": 1,
            "sub_area_id": 1,
            "scheme_id": 1,
            "payment_id": 5,
            "ownership_id": 1,
            "consumer_category_id": 1,
            "sub_category_id": 1,
            "is_vip": True,
            "connectivity": True,
            "registration_channel_id": 1,
            "source_id": 1,
            "registration_date": "30-04-2020",
            "is_active": True,
            "created_by": True,
            "updated_by": True,
            "created_date": True,
            "updated_date": True
        }

    def get_all_registration(self):
        response = client.get(reverse('get_registrations'))
        self.assertEqual(response.status_code, status.HTTP_200)

    def get_single_registration(self):
        response = client.get(reverse('get_registrations', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200)

    def create_registration_valid(self):
        response = client.post(
            reverse('post_registration'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200)

    def create_registration_invalid(self):
        response = client.post(
            reverse('post_registration'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def update_registration_valid_data(self):
        response = client.put(
            reverse('put_registration', kwargs={'pk': 1}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200)

    def update_registration_invalid_data(self):
        response = client.put(
            reverse('put_registration', kwargs={'pk': 20}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, response.status.HTTP_404_NOT_FOUND)
