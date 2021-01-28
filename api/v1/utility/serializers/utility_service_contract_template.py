from rest_framework import serializers, status
from v1.consumer.serializers.consumer_category import ConsumerCategoryViewSerializer
from v1.consumer.serializers.consumer_sub_category import ConsumerSubCategoryViewSerializer
from v1.utility.models.utility_service_contract_template import \
    UtilityServiceContractTemplate as UtilityServiceContractTemplateTbl
from datetime import datetime
from django.db import transaction
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.utility.views.common_functions import set_utility_contract_validated_data
from api.messages import CONTRACT_TEMPLATE_ALREADY_EXIST


class UtilityServiceContractTemplateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityServiceContractTemplateTbl
        fields = '__all__'
