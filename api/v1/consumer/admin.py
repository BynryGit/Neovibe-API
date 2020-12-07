from django.contrib import admin
from v1.complaint.models.complaint_status import ComplaintStatus
from v1.complaint.models.complaint_sub_type import ComplaintSubType
from v1.complaint.models.complaint_type import ComplaintType
from v1.consumer.models.consumer_credit_rating import ConsumerCreditRating
from v1.consumer.models.consumer_down_payment import ConsumerDownPayment
from v1.consumer.models.consumer_loan import ConsumerLoan
from v1.consumer.models.consumer_notification import ConsumerNotification
from v1.consumer.models.consumer_offer_detail import ConsumerOfferDetail
from v1.consumer.models.consumer_offer_master import ConsumerOfferMaster
from v1.consumer.models.consumer_personal_detail import ConsumerPersonalDetail
from v1.consumer.models.consumer_service_contract_details import ConsumerServiceContractDetail
from v1.service.models.consumer_services import ServiceDetails
from v1.consumer.models.consumer_category import ConsumerCategory
from v1.consumer.models.consumer_master import ConsumerMaster
from v1.consumer.models.consumer_meter import ConsumerMeter
from v1.consumer.models.consumer_ownership import ConsumerOwnership
from v1.consumer.models.consumer_scheme_master import ConsumerSchemeMaster
from v1.consumer.models.consumer_status import ConsumerStatus
from v1.consumer.models.consumer_sub_category import ConsumerSubCategory
from v1.consumer.models.consumer_token import ConsumerToken
from v1.consumer.models.financial_details import FinancialDetails
from v1.consumer.models.scheme_type import SchemeType
from v1.consumer.models.service_request_priority import ServiceRequestPriority
from v1.consumer.models.service_request_status import ServiceRequestStatus
from v1.consumer.models.service_status import ServiceStatus
from v1.consumer.models.service_sub_type import ServiceSubType
from v1.consumer.models.source_type import SourceType

admin.site.register(SourceType)
admin.site.register(ComplaintStatus)
admin.site.register(ConsumerOwnership)
admin.site.register(ServiceDetails)
admin.site.register(ConsumerMaster)
admin.site.register(ConsumerMeter)
admin.site.register(ConsumerSchemeMaster)
admin.site.register(ConsumerStatus)
admin.site.register(ConsumerToken)
admin.site.register(FinancialDetails)
admin.site.register(ServiceStatus)
admin.site.register(ServiceRequestPriority)
admin.site.register(ServiceRequestStatus)
admin.site.register(ConsumerCategory)
admin.site.register(ConsumerSubCategory)
admin.site.register(ComplaintType)
admin.site.register(ComplaintSubType)
admin.site.register(ServiceSubType)
admin.site.register(SchemeType)
admin.site.register(ConsumerNotification)
admin.site.register(ConsumerDownPayment)
admin.site.register(ConsumerLoan)
admin.site.register(ConsumerOfferDetail)
admin.site.register(ConsumerOfferMaster)
admin.site.register(ConsumerPersonalDetail)
admin.site.register(ConsumerCreditRating)
admin.site.register(ConsumerServiceContractDetail)
