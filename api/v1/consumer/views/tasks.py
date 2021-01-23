# Function for saving registration timeline
from datetime import datetime
from celery.task import task
from rest_framework import status
from v1.commonapp.models.audit_log import AuditLog
from v1.commonapp.models.module import get_module_by_key
from v1.commonapp.models.sub_module import get_sub_module_by_key
from v1.commonapp.views.custom_exception import CustomAPIException


@task(name="consumer_audit_log")
def save_consumer_audit_log(consumer, field_name, old_value, new_value, remark, user):
    try:
        module = get_module_by_key("CONSUMEROPS")
        sub_module = get_sub_module_by_key("CONSUMER")
        AuditLog(
            tenant=consumer.tenant,
            utility=consumer.utility,
            module_id=module,
            sub_module_id=sub_module,
            object_id=consumer.id,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
            remark=remark,
            log_date=datetime.now(),
            is_active=True,
            created_by=user.id,
            updated_by=user.id,
            created_date=datetime.now(),
            updated_date=datetime.now()
        ).save()
    except Exception as e:
        raise CustomAPIException("Consumer audit log save failed", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
