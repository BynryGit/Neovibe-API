__author__ = "aki"

from celery.task import task
from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.read_cycle import ReadCycle
from v1.meter_data_management.models.schedule_log import ScheduleLog


@task(name="import_consumers")
def create_consumer(schedule_log_obj):
    try:
        schedule_log_obj = ScheduleLog.objects.get(id=schedule_log_obj.id)
        read_cycle_obj = ReadCycle.objects.get(id=schedule_log_obj.read_cycle_id)
        for route in read_cycle_obj.route_json:
            print(route)
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
