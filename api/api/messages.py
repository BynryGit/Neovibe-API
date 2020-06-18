__author__ = 'aki'

from v1.commonapp.models.module import get_module_by_name
from v1.commonapp.models.sub_module import get_sub_module_by_name
from v1.userapp.models.privilege import get_privilege_by_name
from v1.utility.models.utility_master import get_utility_by_name

# *********** MODULE CONSTANTS **************
S_AND_M = get_module_by_name('S&M')
CONSUMER_CARE = get_module_by_name('Consumer Care')
CONSUMER_OPS = get_module_by_name('Consumer Ops')
ADMIN = get_module_by_name('Admin')


# *********** SUB MODULE CONSTANTS **************
DASHBOARD = get_sub_module_by_name('Dashboard')
BILLING = get_sub_module_by_name('Billing')
CAMPAIGN = get_sub_module_by_name('S&M-Campaign')
CONSUMER = get_sub_module_by_name('Consumers')
# CONTRACT = get_sub_module_by_name('S&M-Contract')
# DISPATCHER = get_sub_module_by_name('Dispatcher')
# EMPLOYEE = get_sub_module_by_name('Employee')
# METER_READING = get_sub_module_by_name('Meter reading')
# PAYMENT = get_sub_module_by_name('Payment')
# PAYROLL = get_sub_module_by_name('Payroll')
REGISTRATION = get_sub_module_by_name('Registrations')
REPORTS = get_sub_module_by_name('Reports')
# REQUEST = get_sub_module_by_name('Request')
# SETTING = get_sub_module_by_name('Settings')
# STORE = get_sub_module_by_name('Store')
# SUPPLIER = get_sub_module_by_name('Supplier')
SURVEY = get_sub_module_by_name('S&M-Survey')
# SYSTEM = get_sub_module_by_name('System')
# TENANT = get_sub_module_by_name('Tenant')
# TENDER = get_sub_module_by_name('Tender')
USER = get_sub_module_by_name('Users')
# UTILITY = get_sub_module_by_name('Utility')


# *********** PRIVILEGE CONSTANTS **************
VIEW = get_privilege_by_name('View')
EDIT = get_privilege_by_name('Edit')
DELETE = get_privilege_by_name('Delete')


# *********** UTILITY CONSTANTS **************
MNGL_PUNE = get_utility_by_name('MNGL Pune')
MNGL_MUMBAI = get_utility_by_name('MNGL Mumbai')
BGCL_KOLKATA = get_utility_by_name('BGCL Kolkata')


# *********** KEY CONSTANTS **************
RESULTS='results'
RESULT='result'
MESSAGE='message'
RESPONSE_DATA='response_data'
Token = 'token'
STATE = 'state'
DATA = 'data'
ERROR = 'error'
DUPLICATE = 'duplicate'



# *********** VALUE CONSTANTS **************
UNAUTHORIZED_USER="User is not authorised"
INVALID_TOKEN="User token is not valid"
SUCCESSFUL_LOGIN="User logged in successfully"
SUCCESSFUL_LOGOUT="User logged out successfully"
SUCCESSFULLY_DATA_SAVE='Data has been saved successfully.'
SUCCESSFULLY_DATA_DELETED='Data has been deleted successfully.'
SUCCESSFULLY_DATA_RETRIEVE='Data has been retrieved successfully.'
SUCCESSFULLY_DATA_UPDATED='Data has been updated successfully.'
DATA_ALREADY_DELETE='Data already deleted.'
DATA_ALREADY_EXISTS='Data already exists.'
DATA_NOT_EXISTS='Data not exists.'
AUTODISCOVER_STARTED_SUCCESSFULLY='Autodiscover started successfully'
INVALID_DATA='Invalid data provided, data could not save.'
FAIL= 'fail'
EXIST='exist'
USER_ALREADY_EXIST='User all ready exit with this name.'
SERVER_ERROR='Server error occurred {0}'
INVALID_CREDENTIALS='Provided credentials are wrong.'
SUCCESS = 'success'
EXCEPTION = 'exception'
UNAUTHORIZED = 'Unauthorized'


# *********** CUSTOM CONSTANTS **************
ROLE_PRIVILEGE_NOT_FOUND = 'No Privileges attached to role.'
USER_PRIVILEGE_NOT_FOUND = 'No Privileges assigned to user.'
PRIVILEGE_NOT_FOUND = 'No Privileges found.'
USER_NOT_FOUND = 'User not found.'
ID_STRING_NOT_FOUND = 'Id string not found.'
PRIVILEGE_DELETED = 'Privileges deleted successfully.'
ROLES_DELETED = 'User Roles deleted successfully.'
ROLES_NOT_ASSIGNED = 'No roles assigned to user.'
AREA_NOT_ASSIGNED = 'No areas assigned to user.'
SKILL_NOT_ASSIGNED = 'No skills assigned to user.'
UTILITY_NOT_ASSIGNED = 'No utilities assigned to user.'
NOTES_NOT_FOUND = 'No notes found for user.'
DOCUMENT_NOT_FOUND = 'No Documents found for user.'
