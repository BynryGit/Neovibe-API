__author__ = "aki"

import uuid
import os
from v1.commonapp.models.module import get_module_by_name
from v1.commonapp.models.sub_module import get_sub_module_by_name
from v1.userapp.models.privilege import get_privilege_by_name
from v1.utility.models.utility_master import get_utility_by_name


# *********** MODULE CONSTANTS **************
# S_AND_M = get_module_by_name('S&M')
# CONSUMER_CARE = get_module_by_name('Consumer Care')
CONSUMER_OPS = get_module_by_name('Consumer Ops')
# ADMIN = get_module_by_name('Admin')


# *********** SUB MODULE CONSTANTS **************
# DASHBOARD = get_sub_module_by_name('Dashboard')
# BILLING = get_sub_module_by_name('Billing')
# CAMPAIGN = get_sub_module_by_name('S&M-Campaign')
CONSUMER = get_sub_module_by_name('Consumers')
# CONTRACT = get_sub_module_by_name('S&M-Contract')
# DISPATCHER = get_sub_module_by_name('Dispatcher')
# EMPLOYEE = get_sub_module_by_name('Employee')
# METER_READING = get_sub_module_by_name('Meter reading')
# PAYMENT = get_sub_module_by_name('Payment')
# PAYROLL = get_sub_module_by_name('Payroll')
REGISTRATION = get_sub_module_by_name('Registrations')
# REPORTS = get_sub_module_by_name('Reports')
# REQUEST = get_sub_module_by_name('Request')
# SETTING = get_sub_module_by_name('Settings')
# STORE = get_sub_module_by_name('Store')
# SUPPLIER = get_sub_module_by_name('Supplier')
# SURVEY = get_sub_module_by_name('S&M-Survey')
# SYSTEM = get_sub_module_by_name('System')
# TENANT = get_sub_module_by_name('Tenant')
TENANT = ''
# TENDER = get_sub_module_by_name('Tender')
USER = get_sub_module_by_name('Users')
# UTILITY = get_sub_module_by_name('Utility')


# *********** PRIVILEGE CONSTANTS **************
VIEW = get_privilege_by_name('View')
EDIT = get_privilege_by_name('Edit')
DELETE = get_privilege_by_name('Delete')


# *********** UTILITY CONSTANTS **************
# MNGL_PUNE = get_utility_by_name('MNGL Pune')
# MNGL_MUMBAI = get_utility_by_name('MNGL Mumbai')
# BGCL_KOLKATA = get_utility_by_name('BGCL Kolkata')

ADMIN = 2
# USER = 1
# VIEW = 1
# EDIT = 2

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