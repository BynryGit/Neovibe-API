__author__ = "aki"

import uuid
import os
from v1.commonapp.models.module import get_module_by_name, get_module_by_key
from v1.commonapp.models.sub_module import get_sub_module_by_name, get_sub_module_by_key, get_sub_module_id_by_key
from v1.userapp.models.privilege import get_privilege_by_name, get_privilege_by_key
from v1.utility.models.utility_master import get_utility_by_name

# *********** MODULE CONSTANTS **************
S_AND_M = get_module_by_key('S&M') if get_module_by_key('S&M') else ""
CONSUMER_CARE = get_module_by_key('CONSUMER_CARE') if get_module_by_key('CONSUMER_CARE') else ""
CONSUMER_OPS = get_module_by_key('CONSUMER_OPS') if get_module_by_key('CONSUMER_OPS') else ""
GAS_MANAGEMENT = get_module_by_key('GAS_MANAGEMENT') if get_module_by_key('GAS_MANAGEMENT') else ""
WORK_ORDER = get_module_by_key('WORK_ORDER') if get_module_by_key('WORK_ORDER') else ""
NETWORK = get_module_by_key('NETWORK') if get_module_by_key('NETWORK') else ""
SPEND = get_module_by_key('SPEND') if get_module_by_key('SPEND') else ""
HUMAN_CAPITAL = get_module_by_key('HUMAN_CAPITAL') if get_module_by_key('HUMAN_CAPITAL') else ""
FINANCE = get_module_by_key('FINANCE') if get_module_by_key('FINANCE') else ""
ADMIN = get_module_by_key('ADMIN') if get_module_by_key('ADMIN') else ""
DEMOM = get_module_by_key('DEMOM') if get_module_by_key('DEMOM') else ""

# *********** SUB MODULE CONSTANTS **************
S_AND_M_DASHBOARD = get_sub_module_by_key('S_AND_M_DASHBOARD') if get_sub_module_by_key('S_AND_M_DASHBOARD') else ""
CONSUMER_CARE_DASHBOARD = get_sub_module_by_key('CONSUMER_CARE_DASHBOARD') if get_sub_module_by_key(
    'CONSUMER_CARE_DASHBOARD') else ""
CONSUMER_OPS_DASHBOARD = get_sub_module_by_key('CONSUMER_OPS_DASHBOARD') if get_sub_module_by_key(
    'CONSUMER_OPS_DASHBOARD') else ""
GAS_MANAGEMENT_DASHBOARD = get_sub_module_by_key('GAS_MANAGEMENT_DASHBOARD') if get_sub_module_by_key(
    'GAS_MANAGEMENT_DASHBOARD') else ""
WORK_ORDER_DASHBOARD = get_sub_module_by_key('WORK_ORDER_DASHBOARD') if get_sub_module_by_key(
    'WORK_ORDER_DASHBOARD') else ""
NETWORK_DASHBOARD = get_sub_module_by_key('NETWORK_DASHBOARD') if get_sub_module_by_key('NETWORK_DASHBOARD') else ""
SPEND_DASHBOARD = get_sub_module_by_key('SPEND_DASHBOARD') if get_sub_module_by_key('SPEND_DASHBOARD') else ""
HUMAN_CAPITAL_DASHBOARD = get_sub_module_by_key('HUMAN_CAPITAL_DASHBOARD') if get_sub_module_by_key(
    'HUMAN_CAPITAL_DASHBOARD') else ""
FINANCE_DASHBOARD = get_sub_module_by_key('S_AND_M_DASHBOARD') if get_sub_module_by_key('S_AND_M_DASHBOARD') else ""
METER_DATA = get_sub_module_by_key('METER_DATA') if get_sub_module_by_key('METER_DATA') else ""

BILLING = get_sub_module_by_key('BILLING') if get_sub_module_by_key('BILLING') else ""
CAMPAIGN = get_sub_module_by_key('CAMPAIGN') if get_sub_module_by_key('CAMPAIGN') else ""
CONSUMER = get_sub_module_by_key('CONSUMER') if get_sub_module_by_key('CONSUMER') else ""
CONTRACT = get_sub_module_by_key('CONTRACT') if get_sub_module_by_key('CONTRACT') else ""
DISPATCHER = get_sub_module_by_key('DISPATCHER') if get_sub_module_by_key('DISPATCHER') else ""
EMPLOYEE = get_sub_module_by_key('EMPLOYEE') if get_sub_module_by_key('EMPLOYEE') else ""
METER_READING = get_sub_module_by_key('METER_READING') if get_sub_module_by_key('METER_READING') else ""
PAYMENT = get_sub_module_by_key('PAYMENT') if get_sub_module_by_key('PAYMENT') else ""
PAYROLL = get_sub_module_by_key('PAYROLL') if get_sub_module_by_key('PAYROLL') else ""
S_AND_M_REGISTRATION = get_sub_module_by_key('S_AND_M_REGISTRATION') if get_sub_module_by_key(
    'S_AND_M_REGISTRATION') else ""
CONSUMER_CARE_REGISTRATION = get_sub_module_by_key('CONSUMER_CARE_REGISTRATION') if get_sub_module_by_key(
    'CONSUMER_CARE_REGISTRATION') else ""
CONSUMER_OPS_REGISTRATION = get_sub_module_by_key('CONSUMER_OPS_REGISTRATION') if get_sub_module_by_key(
    'CONSUMER_OPS_REGISTRATION') else ""
REPORTS = get_sub_module_by_key('REPORT') if get_sub_module_by_key('REPORT') else ""
REQUEST = get_sub_module_by_key('REQUEST') if get_sub_module_by_key('REQUEST') else ""
SETTING = get_sub_module_by_key('SETTINGS') if get_sub_module_by_key('SETTINGS') else ""
STORE = get_sub_module_by_key('STORE') if get_sub_module_by_key('STORE') else ""
SUPPLIER = get_sub_module_by_key('SUPPLIER') if get_sub_module_by_key('SUPPLIER') else ""
SURVEY = get_sub_module_by_key('SURVEY') if get_sub_module_by_key('SURVEY') else ""
SYSTEM = get_sub_module_by_key('SYSTEM') if get_sub_module_by_key('SYSTEM') else ""
TENANT = get_sub_module_by_key('TENANT') if get_sub_module_by_key('TENANT') else ""
COMPLAINT = get_sub_module_by_key('COMPLAINT') if get_sub_module_by_key('COMPLAINT') else ""
DEMOSM = get_sub_module_by_key('DEMOSM') if get_sub_module_by_key('DEMOSM') else ""

TENDER = get_sub_module_by_key('TENDER') if get_sub_module_by_key('TENDER') else ""
S_AND_M_USER = get_sub_module_by_key('S_AND_M_USER') if get_sub_module_by_key('S_AND_M_USER') else ""
CONSUMER_CARE_USER = get_sub_module_by_key('CONSUMER_CARE_USER') if get_sub_module_by_key('CONSUMER_CARE_USER') else ""
CONSUMER_OPS_USER = get_sub_module_by_key('CONSUMER_OPS_USER') if get_sub_module_by_key('CONSUMER_OPS_USER') else ""
GAS_MANAGEMENT_USER = get_sub_module_by_key('GAS_MANAGEMENT_USER') if get_sub_module_by_key(
    'GAS_MANAGEMENT_USER') else ""
NETWORK_USER = get_sub_module_by_key('NETWORK_USER') if get_sub_module_by_key('NETWORK_USER') else ""
SPEND_USER = get_sub_module_by_key('SPEND_USER') if get_sub_module_by_key('SPEND_USER') else ""
HUMAN_CAPITAL_USER = get_sub_module_by_key('HUMAN_CAPITAL_USER') if get_sub_module_by_key('HUMAN_CAPITAL_USER') else ""
UTILITY_MASTER = get_sub_module_by_key('UTILITY_MASTER') if get_sub_module_by_key('UTILITY_MASTER') else ""

# *********** PRIVILEGE CONSTANTS **************
VIEW = get_privilege_by_key('VIEW') if get_privilege_by_key('VIEW') else ""
EDIT = get_privilege_by_key('EDIT') if get_privilege_by_key('EDIT') else ""

METER_PICTURE = 'media/meter'


def get_file_name(upload_folder, filename):
    try:
        filename = filename.rsplit('.', 1)
        filename = "%s_%s.%s" % (filename[0], uuid.uuid4(), filename[1])
        return os.path.join(upload_folder, filename)
    except:
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join(upload_folder, filename)
