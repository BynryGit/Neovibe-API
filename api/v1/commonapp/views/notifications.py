import logging
from celery.task import task
from twilio.rest import Client
from v1.commonapp.views.logger import logger
from django.core.mail import EmailMultiAlternatives
from v1.commonapp.views.secret_reader import SecretReader
from v1.utility.models import utility_master
import html
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend
from v1.registration import models
from v1.consumer import models as consumer_model
from v1.work_order import models as work_order_model
# Local logging
local_logger = logging.getLogger('django')
secret_reader = SecretReader()


class OutboundHandler:

    def __init__(self, type, instance):
        self.type = type
        self.instance = instance

    def handle_communications(self):
        dictionary_of_variables = {}
        if self.type == 19:
            utility = utility_master.get_utility_by_id(self.instance.id)
            dictionary_of_variables = {
                "{Utility.email}": utility.email_id,
                "{Utility.utility_name}": utility.name,
            }
        elif self.type == 10:
            registration = models.registrations.get_registration_by_id(self.instance.id)
            dictionary_of_variables = {
                "{Utility.email}": registration.email_id,
                "{Utility.utility_name}": registration.email_id,
            }
        elif self.type == 3:
            consumer = consumer_model.consumer_service_contract_details.get_consumer_service_contract_detail_by_id(self.instance.id)
            dictionary_of_variables = {
                "{Utility.email}": "dummy@gmail.com",
                "{Utility.utility_name}": "dummy",
            }
        elif self.type == 5:
            if self.instance.sa_id:
                appointment_obj = work_order_model.service_assignment.get_service_appointment_by_id(self.instance.sa_id)
            else:
                appointment_obj = work_order_model.service_appointments.get_service_appointment_by_id(self.instance.id)
            dictionary_of_variables = {
            "{appointment.number}" : appointment_obj.sa_number,
            "{appointment.name}" : appointment_obj.sa_name
            }
        return dictionary_of_variables


class EmailHandler(OutboundHandler):
    def __init__(self, type, instance):
        OutboundHandler.__init__(self, type, instance)
        super().__init__(type, instance)

    def html_handler(self, html_template, array):
        # Replace the Keys with their actual values
        for k, v in array.items():
            html_template = html_template.replace(k, array[k])
        return html_template

    @task(name='send_mail')
    def send_email(subject, from_email, to, body=None, attachments=None, html=None):
        try:
            email_host = secret_reader.get_email_host()
            email_port = secret_reader.get_email_port()
            email_username = secret_reader.get_email_host_user()
            print("EMAIL HOST", email_host, "EMAIL PORT", email_port, "EMAIL USER", email_username)
            backend = EmailBackend(host=email_host, port=email_port,
                                   username=email_username, use_tls=True, fail_silently=False)
            print("SUBJECT", subject, "BODY", body, "FROM EMAIL", from_email, "TO_EMAIL", to)
            msg = EmailMultiAlternatives(subject=subject, body=body, from_email=from_email, to=to, connection=backend,
                                         attachments=attachments)
            if html is not None:
                msg.attach_alternative(html, "text/html")
            msg.send(fail_silently=False)
        except Exception as e:
            local_logger.info("In send mail " + str(e))
            logger().log(e, 'LOW')


class SMSHandler(OutboundHandler):
    def __init__(self, type, instance):
        OutboundHandler.__init__(self, type, instance)
        super().__init__(type, instance)

    def html_handler(self, html_template, array):
        # Replace the Keys with their actual values
        for k, v in array.items():
            html_template = html_template.replace(k, array[k])
        return html_template

    @task(name='send_sms')
    def send_sms(self, sms_body, from_number, to_number):
        try:
            account_sid = secret_reader.get_twilio_sid()
            auth_token = secret_reader.get_twilio_token()
            client = Client(account_sid, auth_token)
            print(account_sid, auth_token)
            message = client.messages.create(
                body=sms_body,
                from_=from_number,
                to=to_number
            )
            print(message.sid)
        except Exception as e:
            logger().log(e, 'LOW', message=str(e))
