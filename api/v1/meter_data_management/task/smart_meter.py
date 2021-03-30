__author__ = "aki"

# API Header
# Package: Basic
# Modules: All
# Sub Module: All
# Usage: This task is used to save smart meter data
# Tables used: Consumer Detail
# Author: Akshay
# Created on: 27/03/2021

import requests
from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.consumer_detail import ConsumerDetail as ConsumerDetailTbl
from v1.meter_data_management.models.meter_reading import MeterReading as MeterReadingTbl
from v1.meter_data_management.models.smart_meter_configuration import SmartMeterConfiguration as \
    SmartMeterConfigurationTbl


def smart_meter():
    try:
        consumer_obj = ConsumerDetailTbl.objects.filter(state=1, is_active=True)
        for consumer in consumer_obj:
            smart_meter_url_obj = SmartMeterConfigurationTbl.objects.get(tenant=consumer.tenant,
                                                                         utility=consumer.utility, is_active=True)
            response = requests.post(url=smart_meter_url_obj.api_url, data={'meter_no':consumer.meter_no})
            smart_meter_data = dict(response.json())
            MeterReadingTbl(
                tenant=consumer.tenant,
                utility=consumer.utility,
                consumer_detail_id=consumer.consumer_id,
                read_cycle_id=consumer.read_cycle_id,
                route_id=consumer.route_id,
                utility_product_id=consumer.utility_product_id,
                schedule_log_id=consumer.schedule_log_id,
                current_meter_reading=smart_meter_data['current_reading'],
                current_meter_reading_v1=smart_meter_data['current_reading'],
                current_meter_reading_v2=smart_meter_data['current_reading'],
                consumer_no=smart_meter_data['consumer_no'],
                meter_no=smart_meter_data['meter_no'],
                is_meter_matching=True,
                is_reading_matching=True,
                is_validated=True,
                reading_status=2
            ).save()
    except Exception as ex:
        print(ex)
        logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')


smart_meter()
