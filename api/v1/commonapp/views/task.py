from datetime import datetime

from celery.task import task
from rest_framework import status
from v1.commonapp.models.lifecycle import LifeCycle
from v1.commonapp.models.module import get_module_by_key
from v1.commonapp.models.sub_module import get_sub_module_by_key
from v1.commonapp.views.custom_exception import CustomAPIException


@task(name="admin_timeline", queue='admin_timeline_queue')
def save_admin_timeline(obj, title, text, state, user):
    try:
        module = get_module_by_key("ADMIN")
        sub_module = get_sub_module_by_key("UTILITY_MASTER")
        LifeCycle(
            tenant=obj.tenant,
            # utility=obj.utility,
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
    except Exception as e:
        raise CustomAPIException("Admin timeline save failed", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
