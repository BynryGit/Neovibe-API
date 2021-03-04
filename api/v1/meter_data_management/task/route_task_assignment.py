__author__ = "aki"

# API Header
# Package: Basic
# Modules: All
# Sub Module: All
# Usage: This task is used to create task according route.
# Tables used: ConsumerDetail, RouteTaskAssignment, JobCardTemplate
# Author: Akshay
# Created on: 04/03/2021

import datetime
from celery.task import task
from fcm_django.models import FCMDevice
from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.consumer_detail import ConsumerDetail
from v1.meter_data_management.models.job_card_template import JobCardTemplate
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id
from v1.meter_data_management.models.route_task_assignment import RouteTaskAssignment
from v1.meter_data_management.models.route import get_route_by_id


@task(name="assign-route-task", queue='Dispatch_I')
def assign_route_task(route_task_assignment_id):
    try:
        time = datetime.datetime.now().time().strftime("%H %M")
        t = time.split(" ")
        time_to_sent = t[0] + ':' + t[1]
        json_data = []

        route_task_assignment_obj = RouteTaskAssignment.objects.get(id=route_task_assignment_id, is_active=True)

        task_template_obj = JobCardTemplate.objects.get(tenant=route_task_assignment_obj.tenant,
                                                        utility=route_task_assignment_obj.utility, is_active=True)

        consumer_detail_obj = ConsumerDetail.objects.filter(route_id=route_task_assignment_obj.route_id,
                                                            schedule_log_id=route_task_assignment_obj.schedule_log_id,
                                                            is_active=True)

        for consumer in consumer_detail_obj:
            json_data.append(
                {
                    "consumer_no": consumer.consumer_no,
                    "meter_no": consumer.meter_no,
                    "consumer_detail_id": consumer.id,
                    "schedule_log_id": consumer.schedule_log_id,
                    "read_cycle_id": consumer.read_cycle_id,
                    "route_id": consumer.route_id,
                    "premise_id": consumer.premise_id,
                    "activity_type_id": consumer.activity_type_id,
                    "utility_product_id": consumer.utility_product_id,
                    "route_task_assignment_id": route_task_assignment_obj.id,
                    "is_active": True,
                    "is_completed": False,
                    "is_revisit": False,
                    "status": 'ALLOCATED',
                    "task_template_meter_json": task_template_obj.meter_read_json_obj,
                    "task_template_additional_parameter_json": task_template_obj.additional_parameter_json
                }
            )

        route_task_assignment_obj.consumer_meter_json = json_data
        route_task_assignment_obj.dispatch_status = 2
        route_task_assignment_obj.save()

        read_cycle_obj = get_read_cycle_by_id(route_task_assignment_obj.read_cycle_id)

        route_obj = get_route_by_id(route_task_assignment_obj.route_id)

        message = "For Read Cycle - " + read_cycle_obj.name + " | Route - " + route_obj.label + " | Consumers - " + \
                  str(consumer_detail_obj.count()) + " Are Assigned To You. Please Press Refresh Button.(Time : " + \
                  time_to_sent + ")"

        try:
            device = FCMDevice.objects.get(user_id=route_task_assignment_obj.meter_reader_id)
            try:
                device.send_message(title='Notification-Assign', body=message)
            except Exception as ex:
                print(ex)
                logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
        except Exception as ex:
            print(ex)
            logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')

    except Exception as ex:
        print(ex)
        logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')

        try:
            task_count = len(route_task_assignment_obj.consumer_meter_json)
            if task_count > 0:
                route_task_assignment_obj.consumer_meter_json = []
            route_task_assignment_obj.dispatch_status = 5
            route_task_assignment_obj.save()
        except:
            route_task_assignment_obj.dispatch_status = 5
            route_task_assignment_obj.save()


@task(name="assign-partial-route-task", queue='Dispatch_I')
def assign_partial_route_task(route_task_assignment_id):
    try:
        time = datetime.datetime.now().time().strftime("%H %M")
        t = time.split(" ")
        time_to_sent = t[0] + ':' + t[1]
        json_data = []

        route_task_assignment_obj = RouteTaskAssignment.objects.get(id=route_task_assignment_id, is_active=True)

        task_obj = RouteTaskAssignment.objects.filter(id=route_task_assignment_obj.id, consumer_meter_json__contains=
        [{'is_active': True}, {'is_completed': False}, {'is_revisit': False}], is_active=True).count()

        if task_obj == 0:
            task_template_obj = JobCardTemplate.objects.get(tenant=route_task_assignment_obj.tenant,
                                                            utility=route_task_assignment_obj.utility, is_active=True)

            consumer_detail_obj = ConsumerDetail.objects.filter(route_id=route_task_assignment_obj.route_id,
                                                                schedule_log_id=route_task_assignment_obj.schedule_log_id,
                                                                is_active=True)
            for consumer in consumer_detail_obj:
                json_data.append(
                    {
                        "consumer_no": consumer.consumer_no,
                        "meter_no": consumer.meter_no,
                        "consumer_detail_id": consumer.id,
                        "schedule_log_id": consumer.schedule_log_id,
                        "read_cycle_id": consumer.read_cycle_id,
                        "route_id": consumer.route_id,
                        "premise_id": consumer.premise_id,
                        "activity_type_id": consumer.activity_type_id,
                        "utility_product_id": consumer.utility_product_id,
                        "route_task_assignment_id": route_task_assignment_obj.id,
                        "is_active": True,
                        "is_completed": False,
                        "is_revisit": False,
                        "status": 'ALLOCATED',
                        "task_template_meter_json": task_template_obj.meter_read_json_obj,
                        "task_template_additional_parameter_json": task_template_obj.additional_parameter_json
                    }
                )

            route_task_assignment_obj.consumer_meter_json = json_data

        route_task_assignment_obj.dispatch_status = 2
        route_task_assignment_obj.save()

        read_cycle_obj = get_read_cycle_by_id(route_task_assignment_obj.read_cycle_id)

        route_obj = get_route_by_id(route_task_assignment_obj.route_id)

        message = "For Read Cycle - " + read_cycle_obj.name + " | Route - " + route_obj.label + " | Consumers - " + \
                  str(task_obj) + " Are Assigned To You. Please Press Refresh Button.(Time : " + \
                  time_to_sent + ")"

        try:
            device = FCMDevice.objects.get(user_id=route_task_assignment_obj.meter_reader_id)
            try:
                device.send_message(title='Notification-Assign', body=message)
            except Exception as ex:
                print(ex)
                logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
        except Exception as ex:
            print(ex)
            logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')

    except Exception as ex:
        print(ex)
        logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')

        task_obj = RouteTaskAssignment.objects.filter(id=route_task_assignment_obj.id, consumer_meter_json__contains=
        [{'is_active': True}, {'is_completed': True}, {'is_revisit': False}], is_active=True).count()

        if task_obj == 0:
            dispatch_status = 0
        else:
            dispatch_status = 4

        route_task_assignment_obj.meter_reader_id = None
        route_task_assignment_obj.dispatch_status = dispatch_status
        route_task_assignment_obj.save()
