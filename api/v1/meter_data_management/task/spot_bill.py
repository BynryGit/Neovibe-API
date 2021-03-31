__author__ = "aki"

# API Header
# Package: Basic
# Modules: All
# Sub Module: All
# Usage: This task is used to save spot bill data
# Tables used: Consumer Detail, Spot Bill
# Author: Akshay
# Created on: 30/03/2021

from v1.billing.models.bill import Bill
from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.consumer_detail import ConsumerDetail as ConsumerDetailTbl
from v1.meter_data_management.models.spot_bill import SpotBill as SpotBillTbl


def spot_bill():
    try:
        consumer_obj = ConsumerDetailTbl.objects.filter(is_spot_bill=True, is_active=True)
        for consumer in consumer_obj:
            bill_obj = Bill.objects.filter(consumer_no=consumer.consumer_no, is_active=True).last()
            if SpotBillTbl.objects.filter(tenant=consumer.tenant, utility=consumer.utility,
                                          consumer_detail_id=consumer.id).exists():
                print("Already Exist")
            else:
                SpotBillTbl(
                    tenant=consumer.tenant,
                    utility=consumer.utility,
                    consumer_detail_id=consumer.id,
                    spot_bill_detail=bill_obj.meter_reading,
                    rate_detail=bill_obj.rate_details
                ).save()
    except Exception as ex:
        print(ex)
        logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')


spot_bill()
