__author__ = "priyanka"

from rest_framework import serializers
from v1.commonapp.common_functions import ChoiceField
from v1.commonapp.serializers.global_lookup import GlobalLookupShortViewSerializer
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.billing.models.bill_consumer_detail import BillConsumerDetail
from v1.billing.models.bill_cycle import get_bill_cycle_by_id
from v1.utility.serializers.utility_product import UtilityProductShortViewSerializer
from v1.billing.serializers.bill_cycle import BillCycleShortViewSerializer
from v1.billing.models.bill_schedule_log import ScheduleBillLog
from v1.billing.serializers.bill_schedule import ScheduleBillShortViewSerializer

class ScheduleBillLogShortViewSerializer(serializers.ModelSerializer):
    schedule_bill_id = ScheduleBillShortViewSerializer(many=False, source='get_schedule_bill_name')
    class Meta:
        model = ScheduleBillLog
        fields = ('id_string','schedule_bill_id')


class ScheduleBillLogViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    schedule_bill_id = ScheduleBillShortViewSerializer(many=False, source='get_schedule_bill_name')
    bill_cycle_id = BillCycleShortViewSerializer(many=False, source='get_bill_cycle_name')
    recurring_id = GlobalLookupShortViewSerializer(many=False, source='get_recurring_name')
    utility_product_id = UtilityProductShortViewSerializer(many=False, source='get_utility_product_name')
    schedule_bill_log_status = ChoiceField(choices=ScheduleBillLog.SCHEDULE_BILL_LOG_STATUS)
    total_consumer = serializers.SerializerMethodField()
    

    def get_total_consumer(self, schedule_log_tbl):
        return BillConsumerDetail.objects.filter(bill_schedule_log_id=schedule_log_tbl.id, is_active=True).count()

    class Meta:
        model = ScheduleBillLog
        fields = ('id_string', 'schedule_bill_log_status', 'date_and_time', 'created_date', 'updated_date', 'created_by',
                  'updated_by', 'total_consumer', 'schedule_bill_id','bill_cycle_id', 
                  'recurring_id', 'utility_product_id', 'tenant', 'utility')
