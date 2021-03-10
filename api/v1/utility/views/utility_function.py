from v1.commonapp.models.transition_configuration import TransitionConfiguration, TRANSITION_CHANNEL_DICT, \
    is_transition_configuration_exists
from v1.utility.views.notifications import utility_email_to_admin
from v1.commonapp.views.logger import logger


# Function for performing registration transition events
def perform_events(next_state, utility, transition_object):
    print("JJJJJJHHHEELOOOOKKKK")
    try:
        print(utility)
        if is_transition_configuration_exists(transition_object, next_state, utility):
            print("Inside")

            transition_objs = TransitionConfiguration.objects.filter(transition_object=transition_object,
                                                                     transition_state=next_state,
                                                                     utility=utility, is_active=True)
            for transition_obj in transition_objs:
                if transition_obj.channel == TRANSITION_CHANNEL_DICT['EMAIL']:
                    utility_email_to_admin(utility.id, transition_obj.id)
                if transition_obj.channel == TRANSITION_CHANNEL_DICT['SMS']:
                    pass
                if transition_obj.channel == TRANSITION_CHANNEL_DICT['WHATSAPP']:
                    pass
        else:
            pass
    except Exception as e:
        logger().log(e, 'LOW', module='Consumer Ops', sub_module='Registrations', utility=utility.id)
        pass