import os
from api.settings import prod as settings, settings_dev


class SettingsReader:

    @staticmethod
    def get_secret():
        try:
            if os.environ["smart360_env"] == 'dev':
                return settings_dev.SECRET_KEY
            else:
                return settings.SECRET_KEY
        except:
            pass

    @staticmethod
    def get_twilio_sid():
        try:
            if os.environ["smart360_env"] == 'dev':
                return settings_dev.TWILIO_ACCOUNT_SID
            else:
                return settings.TWILIO_ACCOUNT_SID
        except:
            pass

    @staticmethod
    def get_twilio_token():
        try:
            if os.environ["smart360_env"] == 'dev':
                return settings_dev.TWILIO_AUTH_TOKEN
            else:
                return settings.TWILIO_AUTH_TOKEN
        except:
            pass
