__author__ = "aki"

# API Header
# Package: Basic
# Modules: All
# Sub Module: All
# Usage: This task is used to update task according route.
# Tables used: RouteTaskAssignment
# Author: Akshay
# Created on: 09/03/2021

from celery.task import task
from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.route_task_assignment import get_route_task_assignment_by_id


# todo need to fix json code
@task(name="update-route-task-status", queue='Dispatch_II')
def update_route_task_status(route_task_assignment_id, meter_list):
    try:
        route_task_assignment_obj = get_route_task_assignment_by_id(route_task_assignment_id)

        for meter_no in meter_list:
            task_obj = [x for x in route_task_assignment_obj.consumer_meter_json if x['is_active'] == True and
                        x['meter_no'] == meter_no]
            for task in task_obj:
                task['status'] = 'ASSIGNED'

        route_task_assignment_obj.dispatch_status = 3
        route_task_assignment_obj.save()
    except Exception as ex:
        print(ex)
        logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
