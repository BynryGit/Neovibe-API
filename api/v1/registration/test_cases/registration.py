__author__ = 'aki'

import json
from django.test import TestCase, Client
from django.urls import reverse

# initialize the APIClient app
client = Client()


class RegistrationTestCase(TestCase):

    def setUp(self):
        self.valid_payload = {
            "name" : "GAIL",
			"email_id" : "gail@gmail.com",
			"phone_no" : 7020929071,
			"region_id" : 3,
			"country_id" : 3,
			"state_id" : 1,
			"is_active" : "True"
        }
        self.invalid_payload = {
            "name": "",
			"email_id": "bcgl@gmail.com",
			"phone_no": 8550209071,
			"region_id": 3,
			"country_id": 3,
			"state_id": 3,
			"is_active": "True"
        }

    def get_all_registration(self):
        response = client.get(reverse('enter url name'))
        self.assertEqual(response.data, response.status_code)

    def get_single_registration(self):
        response = client.get(reverse('enter url name', kwargs={'pk': 1}))
        self.assertEqual(response.data, response.status_code)

    def create_valid_registration(self):
        response = client.post(
            reverse('enter url name'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.data, response.status_code)

    def create_invalid_registration(self):
        response = client.post(
            reverse('enter url name'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.data, response.status_code)

    def update_valid_registration(self):
        response = client.put(
            reverse('enter url name', kwargs={'pk': 1}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.data, response.status_code)

    def update_invalid_registration(self):
        response = client.put(
            reverse('enter url name', kwargs={'pk': 20}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.data, response.status_code)