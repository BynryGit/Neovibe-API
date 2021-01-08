__author__ = "aki"

from django.utils import timezone
from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.schedule import Schedule


def create_schedule_log():
    try:
        current_date = timezone.now()
        schedule_obj = Schedule.objects.filter(is_active=True)
    except Exception as ex:
        logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')


create_schedule_log()
