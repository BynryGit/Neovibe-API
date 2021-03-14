__author__ = "aki"

# API Header
# Package: Basic
# Modules: All
# Sub Module: All
# Usage: This task is used to de-assign task.
# Tables used: RouteTaskAssignment
# Author: Akshay
# Created on: 04/03/2021

import datetime
from celery.task import task
from fcm_django.models import FCMDevice
from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id
from v1.meter_data_management.models.route_task_assignment import get_route_task_assignment_by_id
from v1.meter_data_management.models.route import get_route_by_id


# todo need to fix json code
@task(name="de-assign-revisit-task", queue='Dispatch_I')
def de_assign_revisit_task(route_task_assignment_id, meter_no, consumer_no):
    try:
        time = datetime.datetime.now().time().strftime("%H %M")
        t = time.split(" ")
        time_to_sent = t[0] + ':' + t[1]

        route_task_assignment_obj = get_route_task_assignment_by_id(route_task_assignment_id)

        task_obj = [x for x in route_task_assignment_obj.consumer_meter_json if x['is_active'] == True and
                    x['meter_no'] == meter_no and x['consumer_no'] == consumer_no]

        for task in task_obj:
            task['status'] = 'ALLOCATED'
            task['is_revisit'] = True
            task['meter_reader_id'] = None

        route_task_assignment_obj.save()

        read_cycle_obj = get_read_cycle_by_id(route_task_assignment_obj.read_cycle_id)

        route_obj = get_route_by_id(route_task_assignment_obj.route_id)

        message = "For Cycle -" + read_cycle_obj.name + " | Binder -" + route_obj.label + " | Consumers - 1 is " \
                                                                                          "de-assigned from you " \
                                                                                          "Please press refresh" \
                                                                                          " button.(Time : " \
                  + time_to_sent + ")"

        try:
            device = FCMDevice.objects.get(user_id=route_task_assignment_obj.meter_reader_id)
            try:
                device.send_message(title='Notification-De-Assign', body=message)
            except Exception as ex:
                print(ex)
                logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
        except Exception as ex:
            print(ex)
            logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')

    except Exception as ex:
        print(ex)
        logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
