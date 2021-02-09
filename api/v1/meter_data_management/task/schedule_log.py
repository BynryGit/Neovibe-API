__author__ = "aki"

from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from v1.commonapp.views.logger import logger
from v1.commonapp.models.global_lookup import get_global_lookup_by_id
from v1.meter_data_management.models.schedule_log import ScheduleLog
from v1.meter_data_management.models.schedule import Schedule
from v1.meter_data_management.task.consumer_detail import create_consumer


def schedule_log(request):
    try:
        current_date = timezone.now()
        schedule_obj = Schedule.objects.filter(Q(end_date__date__gte=current_date.date()) |
                                               Q(end_date__date=None),
                                               start_date__date__lte=current_date.date(), is_active=True)
        for schedule in schedule_obj:
            recurrence_obj = get_global_lookup_by_id(schedule.recurring_id)
            if recurrence_obj.key == 'no':
                if ScheduleLog.objects.filter(tenant=schedule.tenant, utility=schedule.utility, schedule_id=schedule.id,
                                              is_active=True).exists():
                    print("Schedule Already Exist")
                else:
                    create_schedule_log(schedule)
            else:
                frequency_obj = get_global_lookup_by_id(schedule.frequency_id)
                repeat_every_obj = get_global_lookup_by_id(schedule.repeat_every_id)
                if frequency_obj.key == "daily":
                    if repeat_every_obj.key == "1 day":
                        if ScheduleLog.objects.filter(tenant=schedule.tenant, utility=schedule.utility,
                                                      schedule_id=schedule.id, date_and_time__date=current_date.date(),
                                                      is_active=True).exists():
                            print("Schedule For Current Date Is Already Exist")
                        else:
                            create_schedule_log(schedule)
                    elif repeat_every_obj.key == "2 day":
                        pass
                    elif repeat_every_obj.key == "3 day":
                        pass
                    elif repeat_every_obj.key == "4 day":
                        pass
                    elif repeat_every_obj.key == "5 day":
                        pass
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')


# create_schedule_log()


def create_schedule_log(schedule):
    current_date = timezone.now()
    with transaction.atomic():
        schedule_log_obj = ScheduleLog(tenant=schedule.tenant, utility=schedule.utility, schedule_id=schedule.id,
                                       read_cycle_id=schedule.read_cycle_id, activity_type_id=schedule.activity_type_id,
                                       recurring_id=schedule.recurring_id,
                                       utility_product_id=schedule.utility_product_id, date_and_time=current_date)
        schedule_log_obj.save()
        create_consumer.delay(schedule_log_obj)
