__author__ = 'priyanka'

import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.survey.models.survey_objective import SurveyObjective


class SurveyObjectiveTestCase(APITestCase):
    def get_all_survey_objective(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        utility_obj = UtilityMaster.objects.create(tenant=tenant_obj, name="utility_test")
        SurveyObjective.objects.create(tenant=tenant_obj,utility=utility_obj,objective="Update consumer data")
        response = self.client.get(reverse('survey_objective_list'))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_single_survey_objective(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        utility_obj = UtilityMaster.objects.create(tenant=tenant_obj, name="utility_test")
        survey_objective = SurveyObjective.objects.create(tenant=tenant_obj, utility=utility_obj, objective="Update consumer data")
        response = self.client.get(reverse('survey_objective_detail', args=[survey_objective.id_string]))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
