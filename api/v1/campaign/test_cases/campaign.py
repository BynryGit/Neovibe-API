import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from v1.campaign.models.campaign import Campaign
from v1.userapp.models.user_master import UserDetail


class CampaignListTestCases(APITestCase):
    # def setUp(self):
    #     self.user = UserDetail.objects.create_UserDetail(campaign_name="Smart360 NEW123",start_date="2020-06-13",end_date="2020-07-10",description="This is first entry of POST Method ",
    #             potential_consumers=500,actual_consumers=400,budget_amount="1000",actual_amount=500)
    # def test_campaign(self):
    #     data = {"campaign_name":"Test by priyanka", "start_date":"2020-06-13","end_date":"2020-07-10","description":"This is first entry of POST Method ",
    #             "potential_consumers":800,"actual_consumers":1600,"budget_amount":2400,"actual_amount":3200,
    #             }
    #     response = self.client.post("/api/v1/campaign/", data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def get_all_campaign(self):
        response = self.client.get("/api/v1/campaign/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CampaignTestCases(APITestCase):
    def get_campaign_details(self):
        response = self.client.get(reverse('campaign_data'))
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)