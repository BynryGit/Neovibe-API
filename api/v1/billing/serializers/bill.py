
__author__ = "priyanka"

from django.db import transaction
from django.utils import timezone
from api.messages import DATA_ALREADY_EXISTS
from rest_framework import serializers, status
from v1.commonapp.common_functions import ChoiceField
from v1.commonapp.serializers.global_lookup import GlobalLookupShortViewSerializer
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.billing.models.bill_consumer_detail import BillConsumerDetail as BillConsumerDetailTbl
from v1.billing.serializers.bill_cycle import BillCycleShortViewSerializer
from v1.billing.serializers.bill_schedule_log import ScheduleBillLogShortViewSerializer
from v1.consumer.serializers.consumer_master import ConsumerListSerializer

class ScheduleBillConsumerViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilityMasterViewSerializer(many=False, required=True, source='get_utility')
    bill_cycle_id = BillCycleShortViewSerializer(many=False, source='get_bill_cycle_name')
    bill_schedule_log_id = ScheduleBillLogShortViewSerializer(many=False, source='get_schedule_log')
    consumer_id = ConsumerListSerializer(many=False, source='get_consumer')
    class Meta:
        model = BillConsumerDetailTbl
        fields = ('id_string','tenant','utility','consumer_no','meter_no','bill_cycle_id','bill_schedule_log_id',
        'created_date','consumer_id')