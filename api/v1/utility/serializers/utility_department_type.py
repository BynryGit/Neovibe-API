from rest_framework import serializers, status
from django.db import transaction
from v1.commonapp.common_functions import set_region_validated_data
from datetime import datetime
from api.messages import REGION_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.utility.models.utility_department_type import UtilityDepartmentType as UtilityDepartmentTypeTbl


class UtilityDepartmentTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityDepartmentTypeTbl
        fields = ('name', 'id_string', 'is_active', 'created_by', 'created_date')