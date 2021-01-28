import os
from api.settings import prod, dev
settings = None
if os.environ["smart360_env"] == 'dev':
    settings = dev
if os.environ["smart360_env"] == 'prod':
    settings = prod


class SettingReader:

    @staticmethod
    def get_display_date_format():
        try:
            return settings.DISPLAY_DATE_FORMAT
        except:
            pass

