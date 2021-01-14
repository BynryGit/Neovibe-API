__author__ = "aki"

import uuid
import os
from v1.commonapp.models.module import get_module_by_name, get_module_by_key
from v1.commonapp.models.sub_module import get_sub_module_by_name, get_sub_module_by_key, get_sub_module_id_by_key
from v1.userapp.models.privilege import get_privilege_by_name, get_privilege_by_key
from v1.utility.models.utility_master import get_utility_by_name

# *********** MODULE CONSTANTS **************

S_AND_M = ''
CONSUMER_CARE = ''
CONSUMER_OPS = ''
GAS_MANAGEMENT = ''
WORK_ORDER = ''
NETWORK = ''
SPEND = ''
HUMAN_CAPITAL = ''
FINANCE = ''
ADMIN = ''
DEMOM = ''

# S_AND_M = get_module_by_key('S&M')
# CONSUMER_CARE = get_module_by_key('CONSUMER_CARE')
# CONSUMER_OPS = get_module_by_key('CONSUMER_OPS')
# GAS_MANAGEMENT = get_module_by_key('GAS_MANAGEMENT')
# WORK_ORDER = get_module_by_key('WORK_ORDER')
# NETWORK = get_module_by_key('NETWORK')
# SPEND = get_module_by_key('SPEND')
# HUMAN_CAPITAL = get_module_by_key('HUMAN_CAPITAL')
# FINANCE = get_module_by_key('FINANCE')
# ADMIN = get_module_by_key('ADMIN')
# DEMOM = get_module_by_key('DEMOM')

# *********** SUB MODULE CONSTANTS **************
# S_AND_M_DASHBOARD = get_sub_module_by_key('S_AND_M_DASHBOARD')
# CONSUMER_CARE_DASHBOARD = get_sub_module_by_key('CONSUMER_CARE_DASHBOARD')
# CONSUMER_OPS_DASHBOARD = get_sub_module_by_key('CONSUMER_OPS_DASHBOARD')
# GAS_MANAGEMENT_DASHBOARD = get_sub_module_by_key('GAS_MANAGEMENT_DASHBOARD')
# WORK_ORDER_DASHBOARD = get_sub_module_by_key('WORK_ORDER_DASHBOARD')
# NETWORK_DASHBOARD = get_sub_module_by_key('NETWORK_DASHBOARD')
# SPEND_DASHBOARD = get_sub_module_by_key('SPEND_DASHBOARD')
# HUMAN_CAPITAL_DASHBOARD = get_sub_module_by_key('HUMAN_CAPITAL_DASHBOARD')
# FINANCE_DASHBOARD = get_sub_module_by_key('S_AND_M_DASHBOARD')

# DASHBOARD = ""
# BILLING = ''
# BILLING = get_sub_module_by_key('BILLING')
# CAMPAIGN = get_sub_module_by_key('CAMPAIGN')
# CAMPAIGN = ''
# CONSUMER = get_sub_module_by_key('CONSUMER')
CONSUMER = ''
# CONTRACT = get_sub_module_by_key('CONTRACT')
CONTRACT = ""
# DISPATCHER = get_sub_module_by_key('DISPATCHER')
DISPATCHER = ""
# EMPLOYEE = get_sub_module_by_key('EMPLOYEE')
EMPLOYEE = ""
# METER_READING = get_sub_module_by_key('METER_READING')
METER_DATA = ""
# PAYMENT = get_sub_module_by_key('PAYMENT')
PAYMENT = ""
# PAYROLL = get_sub_module_by_key('PAYROLL')
PAYROLL = ""
# S_AND_M_REGISTRATION = get_sub_module_by_key('S_AND_M_REGISTRATION')
S_AND_M_REGISTRATION = ''
# CONSUMER_CARE_REGISTRATION = get_sub_module_by_key('CONSUMER_CARE_REGISTRATION')
CONSUMER_CARE_REGISTRATION = ''
# CONSUMER_OPS_REGISTRATION = get_sub_module_by_key('CONSUMER_OPS_REGISTRATION')
CONSUMER_OPS_REGISTRATION = ''
REGISTRATION = ""
# REPORTS = get_sub_module_by_name('Reports')
# REQUEST = get_sub_module_by_name('Request')
# SETTING = get_sub_module_by_name('Settings')
# STORE = get_sub_module_by_name('Store')
# SUPPLIER = get_sub_module_by_name('Supplier')
# SURVEY = get_sub_module_by_name('S&M-Survey')
# SYSTEM = get_sub_module_by_name('System')
# TENANT = get_sub_module_by_name('Tenant')
# COMPLAINT = get_sub_module_by_name('Complaint')
COMPLAINT = ''
TENANT = ''
# DEMOSM = get_sub_module_by_key('DEMOSM')
DEMOSM = ''

# TENDER = get_sub_module_by_key('TENDER')
# S_AND_M_USER = get_sub_module_by_key('S_AND_M_USER')
S_AND_M_USER = ''
# CONSUMER_CARE_USER = get_sub_module_by_key('CONSUMER_CARE_USER')
CONSUMER_CARE_USER = ''
# CONSUMER_OPS_USER = get_sub_module_by_key('CONSUMER_OPS_USER')
CONSUMER_OPS_USER = ''
# GAS_MANAGEMENT_USER = get_sub_module_by_key('GAS_MANAGEMENT_USER')
GAS_MANAGEMENT_USER = ''
# NETWORK_USER = get_sub_module_by_key('NETWORK_USER')
NETWORK_USER = ''
# SPEND_USER = get_sub_module_by_key('SPEND_USER')
SPEND_USER = ''
# HUMAN_CAPITAL_USER = get_sub_module_by_key('HUMAN_CAPITAL_USER')
HUMAN_CAPITAL_USER = ''
# UTILITY_MASTER = get_sub_module_by_key('UTILITY_MASTER')
UTILITY_MASTER = ''

# *********** PRIVILEGE CONSTANTS **************
# VIEW = get_privilege_by_key('VIEW')
VIEW = ''
EDIT = ''
# EDIT = get_privilege_by_key('EDIT')
# DELETE = get_privilege_by_key('Delete')
# *********** UTILITY CONSTANTS **************
# MNGL_PUNE = get_utility_by_name('MNGL Pune')
# MNGL_MUMBAI = get_utility_by_name('MNGL Mumbai')
# BGCL_KOLKATA = get_utility_by_name('BGCL Kolkata')
# ADMIN = 2
# # USER = 1
# UTILITY = 1
# # VIEW = 1
# # EDIT = 2
# USER = 1
# # VIEW = 1
# # EDIT = 2
# DEMOM = 11
# DEMOSM = 60
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
