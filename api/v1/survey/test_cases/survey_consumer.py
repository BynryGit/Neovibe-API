__author__ = 'priyanka'

import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.survey.models.survey_consumer import SurveyConsumer
from v1.survey.models.survey import Survey


class SurveyConsumerTestCase(APITestCase):
    def get_all_survey_consumer(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        utility_obj = UtilityMaster.objects.create(tenant=tenant_obj, name="utility_test")
        survey = Survey.objects.create(tenant=tenant_obj,utility=utility_obj,name="Domestic consumer survey")
        SurveyConsumer.objects.create(tenant=tenant_obj,utility=utility_obj,survey_id=survey.id,vendor_id=1,consumer_no="897445565455",first_name="Priyanka",)
        response = self.client.get(reverse('survey_consumer_list'))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_single_survey_consumer(self):
        tenant_obj = TenantMaster.objects.create(name="tenant_test")
        utility_obj = UtilityMaster.objects.create(tenant=tenant_obj, name="utility_test")
        survey = Survey.objects.create(tenant=tenant_obj, utility=utility_obj, name="Domestic consumer survey")
        survey_consumer = SurveyConsumer.objects.create(tenant=tenant_obj, utility=utility_obj, survey_id=survey.id,vendor_id=1,consumer_no="897445565455", first_name="Priyanka", )
        response = self.client.get(reverse('survey_consumer', args=[survey_consumer.id_string]))
        print("response",response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
