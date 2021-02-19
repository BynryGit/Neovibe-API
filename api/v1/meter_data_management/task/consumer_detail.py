__author__ = "aki"

from celery.task import task
from v1.commonapp.views.logger import logger
from v1.commonapp.models.premises import get_premise_by_id_string
from v1.consumer.models.consumer_master import get_consumer_by_id
from v1.meter_data_management.models.consumer_detail import ConsumerDetail as ConsumerDetailTbl
from v1.meter_data_management.models.meter import Meter as MeterTbl
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id
from v1.meter_data_management.models.route import get_route_by_id_string
from v1.meter_data_management.models.schedule_log import ScheduleLog


@task(name="import_consumers")
def create_consumer(schedule_log_obj):
    try:
        schedule_log_obj = ScheduleLog.objects.get(id=schedule_log_obj.id)
        read_cycle_obj = get_read_cycle_by_id(schedule_log_obj.read_cycle_id)
        for route in read_cycle_obj.route_json:
            route_obj = get_route_by_id_string(route['id_string'])
            for premise in route_obj.premises_json:
                premise_obj = get_premise_by_id_string(premise['id_string'])
                meter_obj = MeterTbl.objects.filter(premise_id=premise_obj.id, is_active=True)
                for meter in meter_obj:
                    consumer_meter_obj = ''#todo
                    consumer_obj = get_consumer_by_id(consumer_meter_obj.consumer_id)
                    if ConsumerDetailTbl.objects.filter(consumer_no=consumer_obj.consumer_no, meter_no=meter.meter_no,
                                                        is_active=True).exists():
                        print('Already Exist')
                    else:
                        ConsumerDetailTbl(
                            tenant=route_obj.tenant,
                            utility=route_obj.utility,
                            premise_id=premise_obj.id,
                            read_cycle_id=read_cycle_obj.id,
                            route_id=route_obj.id,
                            activity_type_id=schedule_log_obj.activity_type_id,
                            utility_product_id=schedule_log_obj.utility_product_id,
                            consumer_no=consumer_obj.consumer_no,
                            # first_name=,
                            # middle_name=,
                            # last_name=,
                            # full_name=,
                            email_id=consumer_obj.email_id,
                            phone_mobile_1=consumer_obj.phone_mobile,
                            phone_mobile_2=consumer_obj.phone_landline,
                            # address_line_1=,
                            # meter_digit=meter,
                            meter_no=meter.meter_no,
                            # prev_meter_reading=,
                        ).save()
                        print('Save')
    except Exception as ex:
        print(ex)
        logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
