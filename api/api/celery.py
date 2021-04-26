__author__ = "aki"

import os
import environ
from celery import Celery
from django.conf import settings
from kombu.utils.url import safequote
from kombu import Exchange, Queue

env = environ.Env()
environ.Env.read_env('.env')

# set the default Django settings module for the 'celery' program.
if os.environ["smart360_env"] == 'dev':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings.dev')

if os.environ["smart360_env"] == 'qa':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings.prod')

if os.environ["smart360_env"] == 'uat':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings.prod')

app = Celery('api')

CELERY_CONFIG = {
    "CELERY_TASK_SERIALIZER": "pickle",
    "CELERY_ACCEPT_CONTENT": ['json', 'pickle'],
    "CELERY_RESULT_SERIALIZER": "pickle",
    "CELERY_RESULT_BACKEND": None,
    "CELERY_TIMEZONE": 'UTC',
    "CELERY_ENABLE_UTC": True,
    "CELERY_ENABLE_REMOTE_CONTROL": False,
}

# Todo credentials fetch from .env file
AWS_ACCESS_KEY_ID = safequote('AKIARUU5RUAA6JXDZZGR')
AWS_SECRET_ACCESS_KEY = safequote('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')

CELERY_CONFIG.update(
    **{
        "BROKER_URL": "sqs://{aws_access_key}:{aws_secret_key}@".format(aws_access_key=AWS_ACCESS_KEY_ID,
                                                                        aws_secret_key=AWS_SECRET_ACCESS_KEY,),
        "BROKER_TRANSPORT": "sqs",
        "CELERY_DEFAULT_QUEUE": 'Default_Queue',
        "BROKER_TRANSPORT_OPTIONS": {
            "region": 'us-east-2',
            "visibility_timeout": 60,
            "polling_interval": 60,
        },
    }
)

CELERY_QUEUES = (
    Queue('Default_Queue', Exchange('Default_Queue'), routing_key='Default_Queue'),
    Queue('ImportConsumer', routing_key='ImportConsumer_Tasks'),
    Queue('Dispatch_I', routing_key='Dispatch_I_Tasks'),
    Queue('Dispatch_II', routing_key='Dispatch_II_Tasks'),
    Queue('Timeline_Queue', routing_key='Timeline_Queue_Tasks'),
)

CELERY_ROUTES = {
    # Task Use For MDM Module Start
    'v1.meter_data_management.task.consumer_detail.create_consumer': {
        'queue': 'ImportConsumer',
        'routing_key': 'ImportConsumer_Tasks'
    },
    'v1.meter_data_management.task.assign_route_task.assign_route_task': {
            'queue': 'Dispatch_I',
            'routing_key': 'Dispatch_I_Tasks',
    },
    'v1.meter_data_management.task.assign_partial_route_task.assign_partial_route_task': {
            'queue': 'Dispatch_I',
            'routing_key': 'Dispatch_I_Tasks',
    },
    'v1.meter_data_management.task.de_assign_route_task.de_assign_route_task': {
            'queue': 'Dispatch_I',
            'routing_key': 'Dispatch_I_Tasks',
    },
    'v1.meter_data_management.task.assign_revisit_task.assign_revisit_task': {
            'queue': 'Dispatch_I',
            'routing_key': 'Dispatch_I_Tasks',
    },
    'v1.meter_data_management.task.de_assign_revisit_task.de_assign_revisit_task': {
            'queue': 'Dispatch_I',
            'routing_key': 'Dispatch_I_Tasks',
    },
    'v1.meter_data_management.task.update_route_task_status.update_route_task_status': {
            'queue': 'Dispatch_II',
            'routing_key': 'Dispatch_II_Tasks',
    },
    # Task Use For MDM Module End

    # Task Use For User Module Start
    'v1.userapp.views.task.save_user_timeline': {
            'queue': 'Timeline_Queue',
            'routing_key': 'Timeline_Queue_Tasks',
    },
    # Task Use For User Module End

    # Task Use For CommonApp Module Start
    'v1.commonapp.views.task.save_admin_timeline': {
            'queue': 'Timeline_Queue',
            'routing_key': 'Timeline_Queue_Tasks',
    },
    # Task Use For CommonApp Module End

    # Task Use For Work Order Module Start
    'v1.work_order.views.tasks.save_service_appointment_timeline': {
            'queue': 'Timeline_Queue',
            'routing_key': 'Timeline_Queue_Tasks',
    },
    # Task Use For Work Order Module End

    # Task Use For Billing Module Start
    'v1.billing.task.bill_consumer_detail.create_bill_consumers': {
        'queue': 'ImportConsumer',
        'routing_key': 'ImportConsumer_Tasks'
    },
    # Task Use For Billing Module End
}

app.conf.update(**CELERY_CONFIG)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
