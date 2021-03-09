__author__ = "Chinmay"

from django.core.mail.backends.smtp import EmailBackend
from v1.commonapp.models.email_configurations import EmailConfiguration
from v1.commonapp.models.notification_template import get_notification_template_by_id
from v1.commonapp.models.transition_configuration import get_transition_configuration_by_id
from v1.commonapp.views.logger import logger
from v1.commonapp.views.notifications import send_mail
from v1.utility.models import utility_master



def utility_email_to_admin(utility_id, transition_obj_id):
    try:
        utility_obj = utility_master.get_utility_by_id(utility_id)
        transition_obj = get_transition_configuration_by_id(transition_obj_id)
        html = get_notification_template_by_id(transition_obj.template_id)
        html.template = html.template.replace("{utility_name}", utility_obj.name)
        if EmailConfiguration.objects.filter(tenant=utility_obj.tenant, utility=utility_obj.utility).exists():
            email_configuration_obj = EmailConfiguration.objects.get(tenant=utility_obj.tenant, utility=utility_obj.utility)
            backend = EmailBackend(host=email_configuration_obj.email_host, port=email_configuration_obj.email_port,
                                   username=email_configuration_obj.email_host_user, use_tls=True, fail_silently=False)
            send_mail(subject="subject", body="this is body", from_email=email_configuration_obj.from_email,
                      to=[utility_obj.email_id], connection=backend, html=html)
        else:
            pass
    except Exception as e:
        logger().log(e, 'LOW', module = 'Admin', sub_module = 'Utility Configuration', utility=utility_id)