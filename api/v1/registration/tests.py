import requests
from django.test import TestCase, client, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient


class RegistrationTestCase(TestCase):
    # initialize the APIClient app
    def test_registration(self):
        url = 'http://127.0.0.1:8000/api/v1/registration/'
        data = {
            "first_name": "gwen",
            "last_name": "Miles",
            "phone_mobile": "158546346",
            "area_id": "fa2df0cf-c5f3-4128-8b75-72824b8524c0",
            "utility_id": "57ed8a45-014a-4f72-826a-dcf6824c454e"
        }
        headers = {'token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkX3N0cmluZyI6IjkxZDhjZmE5LWM3ZWUtNGQ1NS04NjE3LWYzNjI2MDg2M2M0OCIsInN0cmluZyI6IjQ1QkZFRiJ9.mNjcisDU9XE-r6KQkkvgF5-hZmh3Vgt4ExNW8K8f0g4"}
        response = requests.post(url,data=data,headers=headers)
        print("############",response.content)

    # def test_registration_list(self):
    #     try:
    #         url = 'http://127.0.0.1:8000/api/v1/registration/list'
    #         factory = APIRequestFactory()
    #         request = factory.get(url, format='json', token="sadsada")
    #         print("@@@@@@@@@@@@@@@@@",request.content_params)
    #     except Exception as e:
    #         print("##############",e)