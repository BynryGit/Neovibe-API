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


def schedule_bill_log():
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
                    print("Bill Schedule Log Already Exist")
                else:
                    schedule_log_obj = ScheduleBillLog(tenant=schedule.tenant, utility=schedule.utility,
                                                      schedule_bill_id=schedule.id, bill_cycle_id=schedule.bill_cycle_id,
                                                      recurring_id=schedule.recurring_id,
                                                      utility_product_id=schedule.utility_product_id,
                                                      date_and_time=datetime.now())
                    schedule_log_obj.save()
                    # Call Consumer Import Job
                    create_bill_consumers.delay(schedule_log_obj.id)
            else:
                croniter_obj = croniter.match(schedule.cron_expression, datetime(datetime.today().year,
                                                                                 datetime.today().month,
                                                                                 datetime.today().day, 22,00,00))
                if croniter_obj:
                    with transaction.atomic():
                        if ScheduleBillLog.objects.filter(tenant=schedule.tenant, utility=schedule.utility,
                                                         schedule_bill_id=schedule.id,
                                                         date_and_time__date=datetime.now().date()).exists():
                            print("Bill Schedule Log Already Exist")
                        else:
                            schedule_log_obj = ScheduleBillLog(tenant=schedule.tenant, utility=schedule.utility,
                                                              schedule_bill_id=schedule.id, bill_cycle_id=schedule.bill_cycle_id,
                                                              recurring_id=schedule.recurring_id,
                                                              utility_product_id=schedule.utility_product_id,
                                                              date_and_time=datetime.now())
                            schedule_log_obj.save()
                            # Call Consumer Import Job
                            create_bill_consumers.delay(schedule_log_obj.id)
                else:
                    print("Cron Expression Not Match")
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='BX', sub_module='Billing')


schedule_bill_log()
