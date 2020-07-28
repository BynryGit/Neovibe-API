__author__ = "Rohan"

from django.core.mail.backends.smtp import EmailBackend
from api.settings import EMAIL_HOST_PASSWORD
from v1.commonapp.models.email_configurations import EmailConfiguration
from v1.commonapp.models.notification_template import get_notification_template_by_id
from v1.commonapp.models.transition_configuration import get_transition_configuration_by_id
from v1.commonapp.views.logger import logger
from v1.commonapp.views.notifications import send_mail
from v1.registration.models import registrations


def registration_email_to_consumer(registration_id, transition_obj_id):
    try:
        registration_obj = registrations.get_registration_by_id(registration_id)
        transition_obj = get_transition_configuration_by_id(transition_obj_id)
        html = get_notification_template_by_id(transition_obj.template_id)
        html.template = html.template.replace("{name}",registration_obj.first_name)
        if EmailConfiguration.objects.filter(tenant = registration_obj.tenant, utility = registration_obj.utility).exists():
            email_configuration_obj = EmailConfiguration.objects.get(tenant = registration_obj.tenant, utility = registration_obj.utility)
            backend = EmailBackend(host = email_configuration_obj.email_host, port = email_configuration_obj.email_port,
                                   username = email_configuration_obj.email_host_user,
                                   password = EMAIL_HOST_PASSWORD, use_tls = True, fail_silently = False)
            send_mail(subject = "subject", body = "this is body", from_email = email_configuration_obj.from_email,
                      to = [registration_obj.email_id], connection = backend, html = html)
        else:
            pass
    except Exception as e:
        logger().log(e, 'LOW', module = 'Consumer Ops', sub_module = 'Registations', registration = registration_id)
