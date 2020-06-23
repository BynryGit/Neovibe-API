__author__ = "aki"

from v1.commonapp.views.logger import logger
from v1.meter_reading.models.bill_cycle_reading_allocation import BillCycleReadingAllocation
from v1.meter_reading.models.meter_reading import MeterReading
from v1.meter_reading.models.validation import Validation


def assign_validation():
    try:
        allocation_obj = BillCycleReadingAllocation.objects.filter(is_active=True)
        for allocation in allocation_obj:
            meter_reading_obj = MeterReading.objects.filter(reading_status_id=1, is_assign_to_v1=False, is_active=True,
                                                            is_duplicate=False, bill_cycle_id=allocation.bill_cycle.id)
            for meter_reading in meter_reading_obj:
                validator_obj = Validation(validator_id=allocation.validator_one.id, month=meter_reading.month,
                                           meter_reading_id=meter_reading.id, created_by=1, assigned_to='v1',
                                           bill_cycle_id=meter_reading.bill_cycle_id, route_id=meter_reading.route_id,
                                           consumer_no=meter_reading.consumer_no)
                validator_obj.save()
                meter_reading.is_assign_to_v1 = True
                meter_reading.save()

            print('Allocate to v1')

            meter_reading_obj = MeterReading.objects.filter(reading_status_id=2, is_assign_to_v2=False, is_active=True,
                                                            is_duplicate=False, bill_cycle_id=allocation.bill_cycle.id)
            for meter_reading in meter_reading_obj:
                validator_obj = Validation(validator_id=allocation.validator_two.id, month=meter_reading.month,
                                           meter_reading_id=meter_reading.id, created_by=1, assigned_to='v2',
                                           bill_cycle_id=meter_reading.bill_cycle_id, route_id=meter_reading.route_id,
                                           consumer_no=meter_reading.consumer_no)
                validator_obj.save()
                meter_reading.is_assign_to_v2 = True
                meter_reading.save()

            print('Allocate to v2')

        print ('Validation Allocation Completed')
    except Exception as ex:
        print(ex)
        logger().log(ex, 'ERROR',)


assign_validation()