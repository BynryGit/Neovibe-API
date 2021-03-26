__author__ = "aki"

# API Header
# Package: Basic
# Modules: All
# Sub Module: All
# Usage: This task is used to save schedule log
# Tables used: Schedule, ScheduleLog
# Author: Akshay
# Created on: 26/03/2021

from datetime import datetime
from croniter import croniter
from django.db import transaction
from django.db.models import Q
from v1.commonapp.views.logger import logger
from v1.commonapp.models.global_lookup import get_global_lookup_by_id
from v1.meter_data_management.models.schedule_log import ScheduleLog as ScheduleLogTbl
from v1.meter_data_management.models.schedule import Schedule as ScheduleTbl
from v1.meter_data_management.task.consumer_detail import create_consumer


def schedule_log():
    try:
        schedule_obj = ScheduleTbl.objects.filter(Q(end_date__date__gte=datetime.now().date()) |
                                               Q(end_date__date=None),
                                               start_date__date__lte=datetime.now().date(), is_active=True)
        for schedule in schedule_obj:
            recurrence_obj = get_global_lookup_by_id(schedule.recurring_id)
            if recurrence_obj.key == 'no':
                if ScheduleLogTbl.objects.filter(tenant=schedule.tenant, utility=schedule.utility,
                                                 schedule_id=schedule.id, is_active=True).exists():
                    print("Schedule Log Already Exist")
                else:
                    schedule_log_obj = ScheduleLogTbl(tenant=schedule.tenant, utility=schedule.utility,
                                                      schedule_id=schedule.id, read_cycle_id=schedule.read_cycle_id,
                                                      activity_type_id=schedule.activity_type_id,
                                                      recurring_id=schedule.recurring_id,
                                                      utility_product_id=schedule.utility_product_id,
                                                      date_and_time=datetime.now())
                    schedule_log_obj.save()
                    # Call Consumer Import Job
                    create_consumer.delay(schedule_log_obj.id)
            else:
                croniter_obj = croniter.match(schedule.cron_expression, datetime(datetime.today().year,
                                                                                 datetime.today().month,
                                                                                 datetime.today().day, 22,00,00))
                if croniter_obj:
                    with transaction.atomic():
                        if ScheduleLogTbl.objects.filter(tenant=schedule.tenant, utility=schedule.utility,
                                                         schedule_id=schedule.id,
                                                         date_and_time__date=datetime.now().date()).exists():
                            print("Schedule Log Already Exist")
                        else:
                            schedule_log_obj = ScheduleLogTbl(tenant=schedule.tenant, utility=schedule.utility,
                                                              schedule_id=schedule.id, read_cycle_id=schedule.read_cycle_id,
                                                              activity_type_id=schedule.activity_type_id,
                                                              recurring_id=schedule.recurring_id,
                                                              utility_product_id=schedule.utility_product_id,
                                                              date_and_time=datetime.now())
                            schedule_log_obj.save()
                            # Call Consumer Import Job
                            create_consumer.delay(schedule_log_obj.id)
                else:
                    print("Cron Expression Not Match")
    except Exception as ex:
        print(ex)
        logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')


schedule_log()
