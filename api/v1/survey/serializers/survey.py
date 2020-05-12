__author__ = "Priyanka"

from django.db import transaction
from rest_framework import serializers
from v1.survey.models.survey import Survey as SurveyTbl


class SurveyViewSerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = SurveyTbl
        fields = ('id_string', 'tenant_name', 'name', 'objective_id', 'description','type_id',
                  'category_id','sub_category_id','no_of_consumers','start_date','end_date','area_id','sub_area_id',
                  'completion_date','status_id')

