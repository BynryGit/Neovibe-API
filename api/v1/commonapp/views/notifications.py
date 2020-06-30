from celery.task import task
from sendgrid import Mail, SendGridAPIClient
from api.settings import EMAIL_HOST_PASSWORD
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
    pass
