from celery.task import task
from sendgrid import Mail, SendGridAPIClient
from twilio.rest import Client
from api.settings import *
from v1.commonapp.views.logger import logger


@task(name = 'send_mail')
def send_mail():
    message = Mail(
        from_email='rohan.wagh@bynry.com',
        to_emails='waghrohan218@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>'),
    try:
        sg = SendGridAPIClient(EMAIL_HOST_PASSWORD)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        logger().log(e, 'LOW', message = str(e))


@task(name = 'send_sms')
def send_sms():
    try:
        account_sid = TWILIO_ACCOUNT_SID
        auth_token = TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body='This will be the body of the new message!',
            from_='+19529554228',
            to='+917020929071'
        )
        print(message.sid)
    except Exception as e:
        logger().log(e, 'LOW', message = str(e))
