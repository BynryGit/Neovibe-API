__author__ = "aki"

import uuid
import os

METER_PICTURE = 'media/meter'


def get_file_name(upload_folder,filename):
    try:
        filename = filename.rsplit('.',1)
        filename = "%s_%s.%s" % (filename[0],uuid.uuid4(),filename[1])
        return os.path.join(upload_folder, filename)
    except:
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join(upload_folder, filename)