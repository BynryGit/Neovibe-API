__author__ = "priyanka"

# API Header
# Package: Basic
# Modules: All
# Sub Module: All
# Usage: This task is used to save bill schedule log
# Tables used: Bill Schedule, ScheduleBillLog, Global Lookup
# Author: Priyanka
# Created on: 08/03/2021

from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from v1.commonapp.views.logger import logger
from v1.commonapp.models.global_lookup import get_global_lookup_by_id
from v1.billing.models.bill_schedule_log import ScheduleBillLog
from v1.billing.models.bill_schedule import ScheduleBill
from v1.billing.task.bill_consumer_detail import create_bill_consumers


def schedule_bill_log(request):
    try:
        current_date = timezone.now()
        schedule_obj = ScheduleBill.objects.filter(Q(end_date__date__gte=current_date.date()) |
                                               Q(end_date__date=None),
                                               start_date__date__lte=current_date.date(), is_active=True)

        for schedule in schedule_obj:
            recurrence_obj = get_global_lookup_by_id(schedule.recurring_id)
            if recurrence_obj.key == 'no':
                if ScheduleBillLog.objects.filter(tenant=schedule.tenant, utility=schedule.utility, bill_schedule_id=schedule.id,
                                              is_active=True).exists():
                    print("Schedule Already Exist")
                else:
                    create_schedule_log(schedule)
            else:
                frequency_obj = get_global_lookup_by_id(schedule.frequency_id)
                repeat_every_obj = get_global_lookup_by_id(schedule.repeat_every_id)
                if frequency_obj.key == "hourly":
                    if repeat_every_obj.key == "1 hour":
                        if ScheduleBillLog.objects.filter(tenant=schedule.tenant, utility=schedule.utility,
                                                      bill_schedule_id=schedule.id, date_and_time__hour=current_date.hour,
                                                      is_active=True).exists():
                            print("Schedule For Hour Is Already Exist")
                        else:
                            create_schedule_log(schedule)
                    elif repeat_every_obj.key == "2 hour":
                        pass
                    elif repeat_every_obj.key == "3 hour":
                        pass
                    elif repeat_every_obj.key == "4 hour":
                        pass
                    elif repeat_every_obj.key == "5 hour":
                        pass
                elif frequency_obj.key == "daily":
                    if repeat_every_obj.key == "1 day":
                        print('*****in if')
                        # if ScheduleBillLog.objects.filter(tenant=schedule.tenant, utility=schedule.utility,
                        #                               bill_schedule_id=schedule.id, date_and_time__date=current_date.date(),
                        #                               is_active=True).exists():
                        #     print("Schedule For Current Date Is Already Exist")
                        # else:
                        print('--------',schedule)
                        create_schedule_log(schedule)
                    elif repeat_every_obj.key == "2 day":
                        pass
                    elif repeat_every_obj.key == "3 day":
                        pass
                    elif repeat_every_obj.key == "4 day":
                        pass
                    elif repeat_every_obj.key == "5 day":
                        pass
                elif frequency_obj.key == "yearly":
                    if repeat_every_obj.key == "1 year":
                        if ScheduleBillLog.objects.filter(tenant=schedule.tenant, utility=schedule.utility,
                                                      schedule_bill_id=schedule.id, date_and_time__year=current_date.year,
                                                      is_active=True).exists():
                            print("Schedule For Hour Is Already Exist")
                        else:
                            create_schedule_log(schedule)
                    elif repeat_every_obj.key == "2 year":
                        pass
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')


# create_schedule_log()


def create_schedule_log(schedule):
    current_date = timezone.now()
    with transaction.atomic():
        try:
            schedule_log_obj = ScheduleBillLog(tenant=schedule.tenant, utility=schedule.utility, schedule_bill_id=schedule.id,
                                           bill_cycle_id=schedule.bill_cycle_id, recurring_id=schedule.recurring_id,
                                           utility_product_id=schedule.utility_product_id, date_and_time=current_date)
            schedule_log_obj.save()
            create_bill_consumers.delay(schedule_log_obj.id)
        except Exception as ex:
            print(ex)
            logger().log(ex, 'MEDIUM', module='Billing', sub_module='Schedule')
