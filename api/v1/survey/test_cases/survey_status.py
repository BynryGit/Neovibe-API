__author__ = 'priyanka'

import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.survey.models.survey_status import SurveyStatus


class SurveyStatusTestCase(APITestCase):
    def get_all_survey_status(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        utility_obj = UtilityMaster.objects.create(tenant=tenant_obj, name="utility_test")
        SurveyStatus.objects.create(tenant=tenant_obj,utility=utility_obj,name="Created")
        response = self.client.get(reverse('survey_status_list'))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_single_survey_status(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        utility_obj = UtilityMaster.objects.create(tenant=tenant_obj, name="utility_test")
        survey_status = SurveyStatus.objects.create(tenant=tenant_obj, utility=utility_obj, name="Assigned")
        response = self.client.get(reverse('survey_status', args=[survey_status.id_string]))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
