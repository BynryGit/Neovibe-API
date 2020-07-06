from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.
from v1.userapp.models.role import Role


# class YourTestClass(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         print("setUpTestData: Run once to set up non-modified data for all class methods.")
#         Role.objects.create(tenant_id=1, utility_id=1, type_id=1, role_ID='MNGL01', role='Distributor', created_by=1, updated_by=1)
#
#     # def setUp(self):
#     #     print("setUp: Run once for every test method to setup clean data.")
#     #     Role.objects.get(role='Distributor')
#
#     def test_role_max_length(self):
#         print("Method: test_role_max_length.")
#         Role.objects.get(role='Distributor')
#         max_length = Role._meta.get_field('role').max_length
#         self.assertEquals(max_length, 100)
#         # self.assertFalse(False)
#
#     def test_false_is_true(self):
#         print("Method: test_false_is_true.")
#         self.assertTrue(True)
#
#     def test_one_plus_one_equals_two(self):
#         print("Method: test_one_plus_one_equals_two.")
#         self.assertEqual(1 + 1, 2)


class UserTestCase(APITestCase):
    def test_login(self):
        url = reverse('log-in')
        data = {'email': 'admin@du.com', 'password': 'badwaik20'}
        response = self.client.post(url, data, format='json')
        print('-----------------',response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
