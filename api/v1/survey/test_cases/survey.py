import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from v1.survey.models.survey import Survey

class SurveyTestCases(APITestCase):
    def get_all_survey(self):
        response = self.client.get(reverse('survey_list'))
        print(json.loads(response))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_survey(self):
    #     data = {"survey_name":"priyanka Testing","start_date":"2022-11-12","end_date":"2022-12-12",
    #             "description":"This Survey for use POST method",
	#             "completion_date":"2023-12-12","no_of_consumers":5000}
    #     response = self.client.post("/api/v1/survey/", data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)