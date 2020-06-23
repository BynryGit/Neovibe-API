__author__ = "aki"

from v1.commonapp.views.logger import logger
from v1.meter_reading.models.consumer import Consumer
from v1.meter_reading.models.jobcard import Jobcard
from v1.meter_reading.models.route_assignment import RouteAssignment
from celery.decorators import task


@task(name="create_job_cards")
def create_job_card(route_assignment_obj, month):
    try:
        route_assignment_obj = RouteAssignment.objects.get(id=route_assignment_obj, month=month, is_active=True)
        consumer_obj = Consumer.objects.filter(route_id=route_assignment_obj.route_id,
                                               bill_month=route_assignment_obj.month)
        for consumer in consumer_obj:
            jobcard_obj = Jobcard(
                bill_cycle_id=route_assignment_obj.bill_cycle_id,
                route_id=route_assignment_obj.route_id,
                consumer_no=consumer.consumer_no,
                consumer_id=consumer.id,
                route_assigned_id=route_assignment_obj.id,
                meter_reader_id=route_assignment_obj.meter_reader_id,
                month=month,
                created_by=1,
            )
            jobcard_obj.save()

        route_assignment_obj.status_id = 2
        route_assignment_obj.save()

        # Todo code for send sms to meter reader

    except Exception as ex:
        logger().log(ex, 'ERROR',)


@task(name="update_job_cards")
def update_job_card(route_assignment_obj, month):
    try:
        route_assignment_obj = RouteAssignment.objects.get(id=route_assignment_obj, month=month, is_active=True)
        Jobcard.objects.filter(billcycle_id=route_assignment_obj.bill_cycle_id, month=month,
                                             route_id=route_assignment_obj.route_id).update(is_active=False)
    except Exception as ex:
        logger().log(ex, 'ERROR',)