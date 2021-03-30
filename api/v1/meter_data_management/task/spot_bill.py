__author__ = "aki"

# API Header
# Package: Basic
# Modules: All
# Sub Module: All
# Usage: This task is used to save spot bill data
# Tables used: Consumer Detail, Spot Bill
# Author: Akshay
# Created on: 30/03/2021

from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.consumer_detail import ConsumerDetail as ConsumerDetailTbl
from v1.meter_data_management.models.spot_bill import SpotBill as SpotBillTbl


def spot_bill():
    try:
        consumer_obj = ConsumerDetailTbl.objects.filter(is_spot_bill=True, is_active=True)
        for consumer in consumer_obj:
            SpotBillTbl(
                tenant=consumer.tenant,
                utility=consumer.utility,
                consumer_detail_id=consumer.consumer_id,
            ).save()
    except Exception as ex:
        print(ex)
        logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')


spot_bill()
