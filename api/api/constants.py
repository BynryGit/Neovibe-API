__author__ = "priyanka"

import uuid
import os
from v1.commonapp.models.module import get_module_by_name, get_module_by_key
from v1.commonapp.models.sub_module import get_sub_module_by_name, get_sub_module_by_key, get_sub_module_id_by_key
from v1.userapp.models.privilege import get_privilege_by_name, get_privilege_by_key
from v1.utility.models.utility_master import get_utility_by_name

# *********** MODULE CONSTANTS **************
DEMOM = get_module_by_key('DEMOM') if get_module_by_key('DEMOM') else ""
CX = get_module_by_key('CX') if get_module_by_key('CX') else ""
MX = get_module_by_key('MX') if get_module_by_key('MX') else ""
BX = get_module_by_key('BX') if get_module_by_key('BX') else ""
WX = get_module_by_key('WX') if get_module_by_key('WX') else ""
AX = get_module_by_key('AX') if get_module_by_key('AX') else ""
SX = get_module_by_key('SX') if get_module_by_key('SX') else ""
USER = get_module_by_key('USER') if get_module_by_key('USER') else ""
ADMIN = get_module_by_key('ADMIN') if get_module_by_key('ADMIN') else ""
REPORT = get_module_by_key('REPORT') if get_module_by_key('REPORT') else ""

# *********** SUB MODULE CONSTANTS **************
DEMOSM = get_sub_module_by_key('DEMOSM') if get_sub_module_by_key('DEMOSM') else ""
DASHBOARD = get_sub_module_by_key('DASHBOARD') if get_sub_module_by_key('DASHBOARD') else ""
CONSUMER_CARE = get_sub_module_by_key('CARE') if get_sub_module_by_key('CARE') else ""
CX_SERVICE = get_sub_module_by_key('CX_SERVICE') if get_sub_module_by_key('CX_SERVICE') else ""
SCHEDULE = get_sub_module_by_key('SCHEDULE') if get_sub_module_by_key('SCHEDULE') else ""
DISPATCH = get_sub_module_by_key('DISPATCH') if get_sub_module_by_key('DISPATCH') else ""
VALIDATION = get_sub_module_by_key('VALIDATION') if get_sub_module_by_key('VALIDATION') else ""
UPLOAD = get_sub_module_by_key('UPLOAD') if get_sub_module_by_key('UPLOAD') else ""
METER_MASTER = get_sub_module_by_key('METER_MASTER') if get_sub_module_by_key('METER_MASTER') else ""
BILLING = get_sub_module_by_key('BILLING') if get_sub_module_by_key('BILLING') else ""
PAYMENT = get_sub_module_by_key('PAYMENT') if get_sub_module_by_key('PAYMENT') else ""
DISPATCHER = get_sub_module_by_key('DISPATCHER') if get_sub_module_by_key('DISPATCHER') else ""
WX_ASSET = get_sub_module_by_key('WX_ASSET') if get_sub_module_by_key('WX_ASSET') else ""
CONTRACT = get_sub_module_by_key('CONTRACT') if get_sub_module_by_key('CONTRACT') else ""
SUPPLIER = get_sub_module_by_key('SUPPLIER') if get_sub_module_by_key('SUPPLIER') else ""
AX_ASSET = get_sub_module_by_key('AX_ASSET') if get_sub_module_by_key('AX_ASSET') else ""
REQUEST = get_sub_module_by_key('REQUEST') if get_sub_module_by_key('REQUEST') else ""
STORE = get_sub_module_by_key('STORE') if get_sub_module_by_key('STORE') else ""
TENDER = get_sub_module_by_key('TENDER') if get_sub_module_by_key('TENDER') else ""
PRODUCT = get_sub_module_by_key('PRODUCT') if get_sub_module_by_key('PRODUCT') else ""
SX_SERVICE = get_sub_module_by_key('SX_SERVICE') if get_sub_module_by_key('SX_SERVICE') else ""
ORDER = get_sub_module_by_key('ORDER') if get_sub_module_by_key('ORDER') else ""
CONTRACT = get_sub_module_by_key('CONTRACT') if get_sub_module_by_key('CONTRACT') else ""
SUPPLIER = get_sub_module_by_key('SUPPLIER') if get_sub_module_by_key('SUPPLIER') else ""
UTILITY_MASTER = get_sub_module_by_key('UTILITY_MASTER') if get_sub_module_by_key('UTILITY_MASTER') else ""


# *********** PRIVILEGE CONSTANTS **************
VIEW = get_privilege_by_key('VIEW') if get_privilege_by_key('VIEW') else ""
EDIT = get_privilege_by_key('EDIT') if get_privilege_by_key('EDIT') else ""

METER_PICTURE = 'Meter-Image'


def get_file_name(upload_folder, filename):
    try:
        filename = filename.rsplit('.', 1)
        filename = "%s_%s.%s" % (filename[0], uuid.uuid4(), filename[1])
        return os.path.join(upload_folder, filename)
    except:
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join(upload_folder, filename)
