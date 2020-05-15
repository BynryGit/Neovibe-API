__author__ = 'priyanka'

import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.survey.models.survey_type import SurveyType


class SurveyTypeTestCase(APITestCase):
    def get_all_survey_type(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        utility_obj = UtilityMaster.objects.create(tenant=tenant_obj, name="utility_test")
        SurveyType.objects.create(tenant=tenant_obj,utility=utility_obj,name="consumer")
        response = self.client.get(reverse('survey_type_list'))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_single_survey_type(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        utility_obj = UtilityMaster.objects.create(tenant=tenant_obj, name="utility_test")
        survey_type = SurveyType.objects.create(tenant=tenant_obj, utility=utility_obj, name="Location")
        response = self.client.get(reverse('survey_type', args=[survey_type.id_string]))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
