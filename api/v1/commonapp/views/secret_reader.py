import os
from api.settings import prod, dev
settings = None
if os.environ["smart360_env"] == 'dev':
    settings = dev
if os.environ["smart360_env"] == 'prod':
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
