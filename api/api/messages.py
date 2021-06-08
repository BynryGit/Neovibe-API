__author__ = 'aki'

# *********** KEY CONSTANTS **************
RESULTS = 'results'
RESULT = 'result'
MESSAGE = 'message'
RESPONSE_DATA = 'response_data'
Token = 'token'
STATE = 'state'
DATA = 'data'
ERROR = 'error'
DUPLICATE = 'duplicate',
ID_STRING = 'id_string'
EMAIL = 'email'
NAME = 'name'
ID = 'id'

# *********** VALUE CONSTANTS **************
UNAUTHORIZED_USER = "User is not authorised"
UNAUTHORIZED_UTILITY = "User not authorised for utility"
INVALID_TOKEN = "User token is not valid"
TOKEN_EXPIRED = "This token is expired. please log in again to continue"
SUCCESSFUL_LOGIN = "User logged in successfully"
SUCCESSFUL_LOGOUT = "User logged out successfully"
SUCCESSFULLY_DATA_SAVE = 'Data has been saved successfully.'
SUCCESSFULLY_DATA_DELETED = 'Data has been deleted successfully.'
SUCCESSFULLY_DATA_RETRIEVE = 'Data has been retrieved successfully.'
SUCCESSFULLY_DATA_UPDATED = 'Data has been updated successfully.'
DATA_ALREADY_DELETE = 'Data already deleted.'
DATA_ALREADY_EXISTS = 'Data already exists.'
DATA_NOT_EXISTS = 'Data not exists.'
AUTODISCOVER_STARTED_SUCCESSFULLY = 'Autodiscover started successfully'
INVALID_DATA = 'Invalid data provided, data could not save.'
FAIL = 'fail'
EXIST = 'exist'
USER_ALREADY_EXIST = 'User all ready exit with this name.'
SERVER_ERROR = 'Server error occurred {0}'
INVALID_CREDENTIALS = 'Provided credentials are wrong.'
SUCCESS = 'success'
EXCEPTION = 'exception'
UNAUTHORIZED = 'Unauthorized'

# *********** USER CUSTOM CONSTANTS **************
BANK_ALREADY_EXISTS = 'Bank detail already exists for specified user'
BANK_NOT_FOUND = 'Bank detail not found for specified user.'
ROLE_PRIVILEGE_NOT_FOUND = 'No Privileges attached to role.'
USER_PRIVILEGE_NOT_FOUND = 'No Privileges assigned to user.'
PRIVILEGE_NOT_FOUND = 'No Privileges found.'
USER_NOT_FOUND = 'User not found.'
ID_STRING_NOT_FOUND = 'Id string not found.'
ROLES_NOT_FOUND = 'No roles found.'
PRIVILEGE_DELETED = 'Privileges deleted successfully.'
ROLES_DELETED = 'User Roles deleted successfully.'
ROLES_NOT_ASSIGNED = 'No roles assigned to user.'
AREA_NOT_ASSIGNED = 'No areas assigned to user.'
SKILL_NOT_ASSIGNED = 'No skills assigned to user.'
UTILITY_NOT_ASSIGNED = 'No utilities assigned to user.'
NO_NOTES_NOT_FOUND = 'No notes found for user.'
NOTES_NOT_FOUND = 'Note not found.'
NO_DOCUMENT_NOT_FOUND = 'No Documents found for user.'
DOCUMENT_NOT_FOUND = 'Document not found.'
UTILITY_NOT_FOUND = "Utility not found"
TENANT_NOT_FOUND = "Tenant not found."
REGION_NOT_FOUND = "Region not found."
USER_ALREADY_EXISTS = "User Already Exists."
AREA_NOT_FOUND = "Area not Found."
SUBAREA_NOT_FOUND = "Subarea not Found."
DIVISION_NOT_FOUND = "Division not Found."
ZONE_NOT_FOUND = "Zone not Found."
DOCUMENT_TYPE_NOT_FOUND = "No record found for user document type"
SERVICE_TYPE_NOT_FOUND = "No record found for user service type"
UTILITY_NOT_FOUND = "Utility not found"
DOCUMENT_TYPE_NOT_FOUND = "No record found for user document type"
SERVICE_TYPE_NOT_FOUND = "No record found for user service type"
ROUTE_NOT_FOUND = "Route Not Found."
MOBILE_ALREADY_EXISTS = "Mobile number already exists!"
CONTRACT_ALREADY_EXISTS = "Contract already exists"
WORK_ORDER_ALREADY_EXIST = "Work Order already Exist"
SERVICE_APPOINTMENT_ALREADY_EXIST = "Service Appointment already Exist"
SCHEDULE_APPOINTMENT_ALREADY_EXIST = "Service Appointment already Exist"
SERVICE_ASSIGNMENT_ALREADY_EXIST = "Service Assignment already Exist"
DEPARTMENT_TYPE_ALREADY_EXIST = "Department Type already Exist"
DEPARTMENT_SUBTYPE_ALREADY_EXIST = "Department SubType already Exist"
DIVISION_ALREADY_EXIST = "Division Already Exist"
HOLIDAY_ALREADY_EXIST = "Holiday Already Exist"
METER_ALREADY_EXIST = "Meter Already Exist"
READ_CYCLE_ALREADY_EXIST = "Read Cycle Already Exist"
SERVICE_DEASSIGNMENT = "Service Deassign Successfully"
CONSUMER_COMPLAINT_ALREADY_EXISTS = "Consumer complaint already exists!"
CONSUMER_SERVICE_ALREADY_EXISTS = "Consumer service already exists!"
CONSUMER_OFFER_ALREADY_EXISTS = "Consumer offer already exists!"
OFFER_TYPE_ALREADY_EXISTS = "Offer Type Already Exist!"
OFFER_SUB_TYPE_ALREADY_EXISTS = "Offer SubType Already Exist!"
INTEGRATION_MASTER_ALREADY_EXIST = "Integration Already Exist"
SMART_METER_CONFIGURATION_ALREADY_EXISTS = "Given Smart Meter Configuration already exist."
# *********** NOT FOUND CONSTANTS **************
SERVICE_ASSIGNMENT_NOT_FOUND = "Service Assignment Not Found"
SERVICE_APPOINTMENT_NOT_FOUND = "Service Appointment Not Found"
COUNTRY_NOT_FOUND = "Country Not Found"
STATE_NOT_FOUND = "State Not Found"
CITY_NOT_FOUND = "City Not Found"
STATUS_NOT_FOUND = "Status Not Found"
MODULE_NOT_FOUND = "Module Not Found"
SUBMODULE_NOT_FOUND = "SubModule Not Found"
SUBSCRIPTION_NOT_FOUND = "Subscription Not Found"
SUBSCRIPTION_PLAN_NOT_FOUND = "Subscription Plan Not Found"
SUBSCRIPTION_RATE_NOT_FOUND = "Subscription Rate Not Found"
BANK_NOT_FOUND_FOR_USER = "Bank Detail Not Found For User"
INVOICE_NOT_FOUND = "Invoice Not Found"
REGISTRATION_NOT_FOUND = "Registration not found"
PAYMENT_NOT_FOUND = "Payment not found"
BILL_NOT_FOUND = "Bill not found"
CONSUMER_NOT_FOUND = "Consumer not found"
COMPLAINT_NOT_FOUND = "Complaint not found"
SCHEME_NOT_FOUND = "Scheme not found"
CONTRACT_TYPE_NOT_FOUND = "Contract Type not found"
CONTRACT_PERIOD_NOT_FOUND = "Contract Period not found"
CONTRACT_SUBTYPE_NOT_FOUND = "Contract SubType not found"
TERMS_AND_CONDITION_NOT_FOUND = "Terms and condition not found"
SUPPLIER_TYPE_NOT_FOUND = "Contract Type not found"
SUPPLIER_SUBTYPE_NOT_FOUND = "Contract SubType not found"
PRODUCT_CATEGORY_NOT_FOUND = "Product Category not found"
PRODUCT_SUBCATEGORY_NOT_FOUND = "Product SubCategory not found"
CONTRACT_NOT_FOUND = "Contract not found"
STORE_TYPE_NOT_FOUND = "Store type not found"
STORE_LOCATION_NOT_FOUND = "Store location not found"
UTILITY_SERVICE_CONTRACT_NOT_FOUND = "Utility service contract not found"
READ_CYCLE_NOT_FOUND = "Read Cycle not found"
Bill_CYCLE_NOT_FOUND = "Bill Cycle not found"
FREQUENCY_NOT_FOUND = "Frequency not found"
UTILITY_HOLIDAY_NOT_FOUND = "Utility Holiday Not found."
UTILITY_WORKING_HOURS_NOT_FOUND = "Utility Working Hours Not found."
SCHEDULE_NOT_FOUND = "Schedule not found"
SCHEDULE_LOG_NOT_FOUND = "Schedule log not found"
CONSUMER_FAQ_NOT_FOUND = "Consumer Faq not found."
CONSUMER_SUPPORT_NOT_FOUND = "Consumer support not found."
ACTIVITY_TYPE_NOT_FOUND = "ACtivity type not found"
REPEAT_FREQUENCY_NOT_FOUND = "Repeat Frequency not found"
SERVICE_CONTRACT_TEMPLATE_NOT_FOUND = "Service Contract Template Not Found."
IS_RECCURING_NOT_FOUND = 'Reccuring Id Not Found'
UTILITY_PRODUCT_NOT_FOUND = 'Utility Product not found'
UTILITY_WITH_GIVEN_DETAILS_ALREADY_EXIST = "Utility with given details already exist"
METER_NOT_FOUND = 'Meter not found'
METER_READER_NOT_FOUND = 'Meter reader not found'
METER_TYPE_NOT_FOUND = 'Meter type not found'
PREMISE_NOT_FOUND = "Premise not found"
METER_MAKE_NOT_FOUND = "Meter Make not found"
METER_READING_NOT_FOUND = "Meter Reading not found"
ROUTE_TASK_ASSIGNMENT_NOT_FOUND = "Route task assignment not found"
METER_STATUS_NOT_FOUND = "Meter Status Not Found."
READER_STATUS_NOT_FOUND = "Reader Status Not Found."
ALLOCATION_IN_PROGRESS = "Allocation is in progress"
READING_NOT_PROVIDED = "Readings data not provided"
DATA_NOT_PROVIDED = "data not provided"
CONSUMER_SERVICE_CONTRACT_DETAIL_NOT_FOUND = "Consumer service contract detail not found"


# *********** ALREADY EXIST CONSTANTS **************
NAME_ALREADY_EXIST = "Name Already Exist"
ACCOUNT_NO_ALREADY_EXIST = "Account Number Already Exist"
INVOICE_ALREADY_EXIST = "Invoice Already Exist"
MODULE_ALREADY_EXIST = "Module Already Exist"
SUBMODULE_ALREADY_EXIST = "SubModule Already Exist"
SUBSCRIPTION_ALREADY_EXIST = "Subscription Already Exist"
TERMS_AND_CONDITION_ALREADY_EXIST = "Terms and Condition Already Exist"
REGION_ALREADY_EXIST = 'Region already exist'
COUNTRY_ALREADY_EXIST = "Country Already Exist"
STATE_ALREADY_EXIST = "State Already Exist"
CITY_ALREADY_EXIST = "City Already Exist"
AREA_ALREADY_EXIST = "Area Already Exist"
SUBAREA_ALREADY_EXIST = "SubArea Already Exist"
PREMISE_ALREADY_EXIST = "Premise Already Exist"
SKILL_ALREADY_EXIST = "Skill Already Exist"
CAMPAIGNSUBTYPE_ALREADY_EXIST = "Campaign Subtype Already Exist"
CAMPAIGN_TYPE_ALREADY_EXIST = "Campaign Type Already Exist"
NUMFORMAT_ALREADY_EXIST = "NumFormat with selected Sub Module Already Exist"
ADVERTISEMENT_TYPE_ALREADY_EXIST = "Advertisement with given type already exist"
ADVERTISEMENT_SUBTYPE_ALREADY_EXIST = "Advertisement with given type and subtype already exist"
SURVEY_TYPE_ALREADY_EXIST = "Survey Type already exist"
SURVEY_SUBTYPE_ALREADY_EXIST = "Survey Subtype already exist"
SURVEY_OBJECTIVE_ALREADY_EXIST = "Survey Objective already exist"
REGISTRATION_TYPE_ALREADY_EXIST = "Registration Type Already Exist"
REGISTRATION_SUBTYPE_ALREADY_EXIST = "Registration Subtype Already Exist"
CHANNEL_ALREADY_EXIST = "Channel Already Exist"
COSUMER_CATEGORY_ALREADY_EXIST = "Consumer Category Already Exist"
COSUMER_SUBCATEGORY_ALREADY_EXIST = "Consumer SubCategory Already Exist"
COSUMER_OWNERSHIP_ALREADY_EXIST = "Consumer OwnerShip Already Exist"
COSUMER_CONSENT_ALREADY_EXIST = "Consumer Consent Already Exist"
COSUMER_SUPPORT_ALREADY_EXIST = "Consumer Support Already Exist"
CONSUMER_FAQ_ALREADY_EXIST = "Consumer FAQ Already Exist"
PAYMENT_TYPE_ALREADY_EXIST = "Payment Type Alreday Exist"
PAYMENT_SUBTYPE_ALREADY_EXIST = "Payment SubType Alreday Exist"
PAYMENT_MODE_ALREADY_EXIST = "Payment Mode Already Exist"
COMPLAINT_TYPE_ALREADY_EXIST = "Complaint Type Already Exist"
COMPLAINT_SUBTYPE_ALREADY_EXIST = "Complaint Subtype Already Exist"
SERVICE_TYPE_ALREADY_EXIST = "Service Type Already Exist"
SERVICE_SUBTYPE_ALREADY_EXIST = "Service Subtype Already Exist"
ZONE_ALREADY_EXIST = "Zone Already Exist"
PRODUCT_ALREADY_EXIST = "Product Already Exist"
ROUTE_ALREADY_EXIST = "Route Already Exist"
DOCUMENT_TYPE_ALREADY_EXIST = "Document Type already Exist"
DOCUMENT_ALREADY_EXIST = "Document Already Exist."
DOCUMENT_SUBTYPE_ALREADY_EXIST = "Document Subtype already Exist"
SERVICE_ALREADY_EXIST = "Service Already Exist"
CONTRACT_ALREADY_EXIST = "Contract Already Exist"
CONTRACT_TEMPLATE_ALREADY_EXIST = "Contract Template Already Exist."
NOTIFICATION_TYPE_ALREADY_EXIST = "Notification Type Already Exist."
NOTIFICATION_SUBTYPE_ALREADY_EXIST = "Notification SubType Already Exist."
UTILITY_MODULE_ALREADY_EXIST = "Utility Module Already Exist"
COMPLAINT_MASTER_ALREADY_EXIST = "Complaint Master Already Exist"
METER_READING_ALREADY_EXIST = "Meter reading Already Exist"
ROUTE_TASK_ASSIGNMENT_ALREADY_EXIST = "Route task assignment Already Exist"
JOB_CARD_TEMPLATE_ALREADY_EXISTS = "Template Already Exist."
WORK_ORDER_TYPE_ALREADY_EXIST = "Work Order Type Already Exist."
WORK_ORDER_SUB_TYPE_ALREADY_EXIST = "Work Order Sub Type Already Exist."
READER_STATUS_ALREADY_EXIST = "Reader Status Already Exist."
NOTIFICATION_TEMPLATE_ALREADY_EXIST = "Notification Template Already Exist."
CONTACT_DATA_WITH_EMAIL_ALREADY_EXIST = "Contact Us Details Already Exist."
TIP_ALREADY_EXIST = "Tip Already Exists."


# *********** TRANSITION CONSTANTS **************
SCHEDULE_LOG_TRANSITION = "Schedule Log transition failed."
ROUTE_TASK_ASSIGNMENT_TRANSITION = "Route Task Assignment transition failed."
