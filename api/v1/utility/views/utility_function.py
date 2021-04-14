from v1.commonapp.models.transition_configuration import TransitionConfiguration, TRANSITION_CHANNEL_DICT, \
    is_transition_configuration_exists
from v1.commonapp.views.logger import logger
# from v1.commonapp.views.notifications import handle_communications, html_handler
from v1.commonapp.views.notifications import OutboundHandler, EmailHandler, SMSHandler
from v1.commonapp.models.notification_template import get_notification_template_by_id
from v1.commonapp.models.transition_configuration import get_transition_configuration_by_id
# from v1.commonapp.views.notifications import send_email
# from v1.commonapp.views.notifications import send_sms
from v1.commonapp.views.secret_reader import SecretReader
from master import models


# Function for performing utility transition events
def perform_events(next_state, utility, transition_object):
    try:

        if TransitionConfiguration.objects.filter(transition_object=transition_object, transition_state=next_state,
                                                  tenant=utility.tenant, is_active=True).exists():

            transition_objs = TransitionConfiguration.objects.filter(transition_object=transition_object,
                                                                     transition_state=next_state,
                                                                     tenant=utility.tenant, is_active=True)
            for transition_obj in transition_objs:
                if transition_obj.channel == TRANSITION_CHANNEL_DICT['EMAIL']:
                    transition_obj = get_transition_configuration_by_id(transition_obj.id)
                    # Call to the first function
                    e1 = EmailHandler(transition_obj.transition_object, utility)

                    array = e1.handle_communications()

                    html = get_notification_template_by_id(transition_obj.template_id)

                    email_body = e1.html_handler(html.template, array)

                    e1.send_email('Utility Created SuccessFully', SecretReader.get_from_email(),
                                  [utility.email_id], None, None, email_body)

                if transition_obj.channel == TRANSITION_CHANNEL_DICT['SMS']:
                    # Call to the first function
                    e1 = SMSHandler(transition_obj.transition_object, utility)

                    array = e1.handle_communications()

                    transition_obj = get_transition_configuration_by_id(transition_obj.id)

                    html = get_notification_template_by_id(transition_obj.template_id)

                    sms_body = e1.html_handler(html.template, array)
                    print("SMS Body", utility.phone_no)
                    e1.send_sms(sms_body, SecretReader.get_from_number(),
                                utility.phone_no)
        else:
            pass
    except Exception as e:
        logger().log(e, 'LOW', module='Admin', sub_module='Utility Configuration')
        pass
