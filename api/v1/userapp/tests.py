from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.

class UserTestCase(APITestCase):

    def test_create_user(self):
        url = 'http://127.0.0.1:8000/api/v1/user/'
        data = {
            "city_id":"8961d794-f03e-49b2-a694-7f3aec447b41",
            "user_type_id":"46bf5bc7-bba8-4def-8a83-3b538f0c8bce",
            "user_subtype_id":"c8cd3449-df8b-4ed2-bebc-121ea2b71a4b",
            "form_factor_id":"1735f7cc-8029-4754-855a-67532ecc0257",
            "department_id":"ff00b47d-d735-4fce-aed0-1a7269b1ecf5",
            "status_id":"ec3afefb-aebe-4c02-8ad0-889c3cab341f",
            "first_name":"arpita",
            "middle_name":"ghansham",
            "last_name":"badwaik",
            "phone_mobile":"8483003577",
            "phone_landline":"8483003504",
            "password":"badwaik20",
            "email": "admin@du.com"
        }
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjEwZTk0MjUyLTc5OTEtNGY3Mi1iNzNmLTg0Mjk1OTY5ZTI3OSIsInN0cmluZyI6IjhERjQxRCJ9.AhcENQ_yUZ7z4vuWwDFnwmcqpRr_nAqxsmmoi5l4pok'
        headers = {'token': token}
        response = self.client.post(url, data, format='json', **{'token': token})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_list(self):
        url = 'http://127.0.0.1:8000/api/v1/user/list/'
        response = self.client.get(url, format='json')
        print('------------', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login(self):
        url = 'http://127.0.0.1:8000/api/v1/user/login/'
        data = {'email': 'admin@du.com', 'password': 'badwaik20'}
        response = self.client.post(url, data, format='json')
        print('------------',response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
