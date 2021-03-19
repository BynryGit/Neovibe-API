__author__ = "aki"

import datetime
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from fcm_django.models import FCMDevice
from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.meter_reading import MeterReading as MeterReadingTbl
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id
from v1.meter_data_management.models.route import get_route_by_id
from v1.meter_data_management.models.route_task_assignment import get_route_task_assignment_by_id
from v1.meter_data_management.views.common_function import set_meter_reading_validation_revisit_validated_data


class MeterReadingValidationRevisitSerializer(serializers.ModelSerializer):
    utility_id = serializers.UUIDField(required=True)

    class Meta:
        model = MeterReadingTbl
        fields = ('__all__')

    def update(self, instance, validated_data, user):
        validated_data = set_meter_reading_validation_revisit_validated_data(validated_data)

        with transaction.atomic():
            meter_reading_obj = super(MeterReadingValidationRevisitSerializer, self).update(instance, validated_data)

            meter_reading_obj.updated_by = user.id
            meter_reading_obj.updated_date = timezone.now()
            meter_reading_obj.reading_status = 3
            meter_reading_obj.is_active = False

            route_task_assignment_obj = get_route_task_assignment_by_id(meter_reading_obj.route_task_assignment_id)

            task_obj = [x for x in route_task_assignment_obj.consumer_meter_json if x['is_active'] == True and
                        x['meter_no'] == meter_reading_obj.meter_no]

            for task in task_obj:
                task['status'] = 'ALLOCATED'
                task['is_revisit'] = True
                task['meter_reader_id'] = route_task_assignment_obj.meter_reader_id

            route_task_assignment_obj.save()
            meter_reading_obj.save()

            read_cycle_obj = get_read_cycle_by_id(route_task_assignment_obj.read_cycle_id)

            route_obj = get_route_by_id(route_task_assignment_obj.route_id)

            time = datetime.datetime.now().time().strftime("%H %M")
            t = time.split(" ")
            time_to_sent = t[0] + ':' + t[1]

            message = "For Cycle -" + read_cycle_obj.name + " | Binder -" + route_obj.label + " | Consumers - 1 is " \
                                                                                              "assigned to you " \
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

            return meter_reading_obj
