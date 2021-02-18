from datetime import datetime

from celery.task import task
from rest_framework import status
from v1.commonapp.models.lifecycle import LifeCycle
from v1.commonapp.models.module import get_module_by_key
from v1.commonapp.models.sub_module import get_sub_module_by_key
from v1.commonapp.views.custom_exception import CustomAPIException

from v1.work_order.models.scheduled_appointment import ScheduledAppointment as ScheduledAppointmentTbl
from v1.work_order.serializers.service_assignment import ServiceAssignmentSerializer,ServiceAssignmentViewSerializer
from v1.work_order.models.service_assignment import get_service_assignment_by_appointment_id, SERVICE_ASSIGNMENT_DICT, get_service_assignment_by_id_string
from v1.work_order.models.service_appointments import get_service_appointment_by_id_string, SERVICE_APPOINTMENT_DICT
from django.db import transaction
from master.models import get_user_by_id_string,get_user_by_id

def schedule_appointment_assign():
    try:
        schedule_objs = ScheduledAppointmentTbl.objects.filter(assignment_date__date = date.today(),is_active=True)
        if schedule_objs:
            data = {}
            for schedule_obj in schedule_objs:
                for appointments in schedule_obj.appointments:
                    service_appoint_obj = get_service_appointment_by_id_string(appointments)
                    data['utility_id'] = str(schedule_obj.utility.id_string)
                    data['sa_id'] = str(service_appoint_obj.id_string)
                    data['user_id'] = str(get_user_by_id(schedule_obj.user_id).id_string)
                    data['assignment_date'] = str(schedule_obj.assignment_date)
                    data['assignment_time'] = str(datetime.now().time())
                    assignment_serializer = ServiceAssignmentSerializer(data=data)
                    user = get_user_by_id(schedule_obj.created_by)
                    if assignment_serializer.is_valid(raise_exception=True):
                        with transaction.atomic():                    
                            assignment_obj = assignment_serializer.create(assignment_serializer.validated_data, user)
                            
                            # State change for service assignment start
                            assignment_obj.change_state(SERVICE_ASSIGNMENT_DICT["ASSIGNED"])
                            # State change for service assignment end

                            # State change for service appointment start
                            service_appoint_obj.change_state(SERVICE_APPOINTMENT_DICT["ASSIGNED"])
                            # State change for service appointment end             
        else:
            pass       
        
    except Exception as e:        
        pass

schedule_appointment_assign()



@task(name="service_appointment_timeline")
def save_service_appointment_timeline(obj, title, text, state, user):
    try:
        print('************')
        module = get_module_by_key("WORK_ORDER")
        sub_module = get_sub_module_by_key("DISPATCHER")
        print('*****module*******',module)
        LifeCycle(
            tenant=obj.tenant,
            utility=obj.utility,
            module_id=module.id,
            sub_module_id=sub_module.id,
            object_id=obj.id,
            title=title,
            lifecycle_text=text,
            state=state,
            log_date=datetime.now(),
            is_active=True,
            created_by=user.id,
            updated_by=user.id,
            created_date=datetime.now(),
            updated_date=datetime.now()
        ).save()
        print('////////save/////////',LifeCycle)
    except Exception as e:
        print('............',e)
        raise CustomAPIException("Service Appointment timeline save failed", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
