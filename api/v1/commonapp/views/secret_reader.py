import os
from api.settings import prod
settings = None
if os.environ["smart360_env"] == 'dev':
    from api.settings import dev
    settings = dev
if os.environ["smart360_env"] == 'prod':
    settings = prod
if os.environ["smart360_env"] == 'qa':
    settings = prod

class SecretReader:

    @staticmethod
    def get_secret():
        try:
            return settings.SECRET_KEY
        except:
            pass

    @staticmethod
    def get_twilio_sid():
        try:
            return settings.TWILIO_ACCOUNT_SID
        except:
            pass

    @staticmethod
    def get_twilio_token():
        try:
            return settings.TWILIO_AUTH_TOKEN
        except:
            pass

    @staticmethod
    def get_email_backend():
        try:
            print("EMAIL BACKEND CALLED")
            return settings.EMAIL_BACKEND
        except:
            pass

    @staticmethod
    def get_email_host():
        try:
            print("EMAIL HOST CALLED")
            return settings.EMAIL_HOST
        except:
            pass

    @staticmethod
    def get_email_port():
        try:
            return settings.EMAIL_PORT
        except:
            pass

    @staticmethod
    def get_email_host_user():
        try:
            return settings.EMAIL_HOST_USER
        except:
            pass

    @staticmethod
    def get_from_email():
        try:
            return settings.FROM_EMAIL
        except:
            pass

    @staticmethod
    def get_from_number():
        try:
            return settings.FROM_NUMBER
        except:
            pass
