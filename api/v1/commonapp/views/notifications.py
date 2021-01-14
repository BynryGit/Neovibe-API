import logging
from celery.task import task
from twilio.rest import Client
from v1.commonapp.views.logger import logger
from django.core.mail import EmailMultiAlternatives
from v1.commonapp.views.settings_reader import SettingsReader

# Local logging
local_logger = logging.getLogger('django')
settings_reader = SettingsReader()


@task(name='send_mail')
def send_mail(subject, body, from_email, to, connection=None, attachments=None, cc=None, html=None):
    try:
        msg = EmailMultiAlternatives(subject=subject, body=body, from_email=from_email, to=to, connection=connection,
                                     attachments=attachments)
        if html is not None:
            msg.attach_alternative(html, "text/html")
        msg.send(fail_silently=False)
    except Exception as e:
        local_logger.info("In send mail " + str(e))
        logger().log(e, 'LOW')


@task(name='send_sms')
def send_sms():
    try:
        account_sid = settings_reader.get_twilio_sid()
        auth_token = settings_reader.get_twilio_token()
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body='This will be the body of the new message!',
            from_='+19529554228',
            to='+917020929071'
        )
        print(message.sid)
    except Exception as e:
        logger().log(e, 'LOW', message=str(e))
