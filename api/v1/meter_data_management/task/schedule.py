__author__ = "aki"

from django.utils import timezone
from v1.commonapp.views.logger import logger
from v1.commonapp.models.global_lookup import get_global_lookup_by_id
from v1.meter_data_management.models.schedule_log import ScheduleLog
from v1.meter_data_management.models.schedule import Schedule


def create_schedule_log():
    try:
        current_date = timezone.now()
        schedule_obj = Schedule.objects.filter(start_date__lte=current_date,end_date__gte=current_date,is_active=True)
        for schedule in schedule_obj:
            frequency_obj = get_global_lookup_by_id(schedule.frequency_id)
            if frequency_obj.key == "daily":
                if ScheduleLog.objects.filter(tenant=schedule.tenant, utility=schedule.utility, schedule_id=schedule.id,
                                              read_cycle_id=schedule.read_cycle_id, is_active=True,
                                              date_and_time__date=current_date.date()).exists():
                    print("date aleready Exist")
                else:
                    ScheduleLog(
                        tenant=schedule.tenant,
                        utility=schedule.utility,
                        schedule_id=schedule.id,
                        read_cycle_id=schedule.read_cycle_id,
                        date_and_time=current_date,
                    ).save()
            elif frequency_obj.key == "monthly":
                if ScheduleLog.objects.filter(tenant=schedule.tenant, utility=schedule.utility, schedule_id=schedule.id,
                                              read_cycle_id=schedule.read_cycle_id, is_active=True,
                                              date_and_time__month=current_date.month).exists():
                    print("month Aleready Exist")
                else:
                    ScheduleLog(
                        tenant=schedule.tenant,
                        utility=schedule.utility,
                        schedule_id=schedule.id,
                        read_cycle_id=schedule.read_cycle_id,
                        date_and_time=current_date,
                    ).save()
            elif frequency_obj.key == "yearly":
                if ScheduleLog.objects.filter(tenant=schedule.tenant, utility=schedule.utility, schedule_id=schedule.id,
                                              read_cycle_id=schedule.read_cycle_id, is_active=True,
                                              date_and_time__year=current_date.year).exists():
                    print("year Aleready Exist")
                else:
                    ScheduleLog(
                        tenant=schedule.tenant,
                        utility=schedule.utility,
                        schedule_id=schedule.id,
                        read_cycle_id=schedule.read_cycle_id,
                        date_and_time=current_date,
                    ).save()
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')


create_schedule_log()
