__author__ = "aki"

import uuid
import os
from v1.commonapp.models.module import get_module_by_name
from v1.commonapp.models.sub_module import get_sub_module_by_name, get_sub_module_by_key, get_sub_module_id_by_key
from v1.userapp.models.privilege import get_privilege_by_name
from v1.utility.models.utility_master import get_utility_by_name


# *********** MODULE CONSTANTS **************
# S_AND_M = get_module_by_name('S&M')
S_AND_M = ""
# CONSUMER_CARE = get_module_by_name('Consumer Care')
CONSUMER_CARE = ""
# CONSUMER_OPS = get_module_by_name('Consumer Ops')
CONSUMER_OPS = 3
# ADMIN = get_module_by_name('Admin')
ADMIN = 1

# *********** SUB MODULE CONSTANTS **************
# DASHBOARD = get_sub_module_by_name('Dashboard')
DASHBOARD = ""
# BILLING = get_sub_module_by_name('Billing')
BILLING = ""
# CAMPAIGN = get_sub_module_by_name('S&M-Campaign')
CAMPAIGN = ""
# CONSUMER = get_sub_module_by_name('Consumers')
CONSUMER = ''
# CONTRACT = get_sub_module_by_name('S&M-Contract')
CONTRACT = ""
# DISPATCHER = get_sub_module_by_name('Dispatcher')
DISPATCHER = ""
# EMPLOYEE = get_sub_module_by_name('Employee')
EMPLOYEE = ""
# METER_READING = get_sub_module_by_name('Meter reading')
METER_READING = ""
# PAYMENT = get_sub_module_by_name('Payment')
PAYMENT = ""
# PAYROLL = get_sub_module_by_name('Payroll')
PAYROLL = ""
# REGISTRATION = get_sub_module_id_by_key('REGISTRATION')
REGISTRATION = 10
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
# TENDER = get_sub_module_by_name('Tender')
# USER = get_sub_module_by_name('Users')
# UTILITY = get_sub_module_by_name('Utility')
UTILITY = 1

# *********** PRIVILEGE CONSTANTS **************
# VIEW = get_privilege_by_name('View')
# EDIT = get_privilege_by_name('Edit')
# DELETE = get_privilege_by_name('Delete')


# *********** UTILITY CONSTANTS **************
# MNGL_PUNE = get_utility_by_name('MNGL Pune')
# MNGL_MUMBAI = get_utility_by_name('MNGL Mumbai')
# BGCL_KOLKATA = get_utility_by_name('BGCL Kolkata')

# ADMIN = 2
# USER = 1
# UTILITY = 1
# VIEW = 1
# EDIT = 2
USER = ''
VIEW = ''
EDIT = 1

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