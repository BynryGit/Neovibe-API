from v1.commonapp.models.transition_configuration import TransitionConfiguration, TRANSITION_CHANNEL_DICT, \
    is_transition_configuration_exists
from v1.utility.views.notifications import utility_email_to_admin
from v1.commonapp.views.logger import logger


# Function for performing registration transition events
def perform_events(next_state, utility, transition_object):
    print("JJJJJJHHHEELOOOOKKKK")
    try:
        print(utility)
        if TransitionConfiguration.objects.filter(transition_object=transition_object, transition_state=next_state,
                                                  tenant=utility.tenant, is_active=True).exists():

            print("Inside")

            transition_objs = TransitionConfiguration.objects.filter(transition_object=transition_object,
                                                                     transition_state=next_state,
                                                                     tenant=utility.tenant, is_active=True)
            print(transition_objs)
            for transition_obj in transition_objs:
                if transition_obj.channel == TRANSITION_CHANNEL_DICT['EMAIL']:
                    print("DDDOOONNNE")
                    utility_email_to_admin(utility, transition_obj.id)
                if transition_obj.channel == TRANSITION_CHANNEL_DICT['SMS']:
                    pass
                if transition_obj.channel == TRANSITION_CHANNEL_DICT['WHATSAPP']:
                    pass
        else:
            pass
    except Exception as e:
        logger().log(e, 'LOW', module='Consumer Ops', sub_module='Registrations')
        pass