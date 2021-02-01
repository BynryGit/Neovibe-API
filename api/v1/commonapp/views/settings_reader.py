import os
from api.settings import prod
settings = None
if os.environ["smart360_env"] == 'dev':
    from api.settings import dev
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

