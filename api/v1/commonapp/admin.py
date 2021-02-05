from django.contrib import admin
from v1.commonapp.models.area import Area
from v1.commonapp.models.audit_log import AuditLog
from v1.commonapp.models.city import City
from v1.commonapp.models.zone import Zone
from v1.commonapp.models.country import Country
from v1.commonapp.models.currency import Currency
from v1.commonapp.models.department import Department
from v1.commonapp.models.department_subtype import DepartmentSubtype
from v1.commonapp.models.document import Document
from v1.commonapp.models.document_sub_type import DocumentSubType
from v1.commonapp.models.document_type import DocumentType
from v1.commonapp.models.email_configurations import EmailConfiguration
from v1.commonapp.models.form_factor import FormFactor
from v1.commonapp.models.module import Module
from v1.commonapp.models.notes import Notes
from v1.commonapp.models.notification import Notification
from v1.commonapp.models.notification_template import NotificationTemplate
from v1.commonapp.models.region import Region
from v1.commonapp.models.service_request_type import ServiceType
from v1.commonapp.models.service_request_sub_type import ServiceSubTypes
from v1.commonapp.models.skills import Skills
from v1.commonapp.models.state import State
from v1.commonapp.models.premises import Premise
from v1.commonapp.models.state_configuration import StateConfiguration
from v1.commonapp.models.sub_area import SubArea
from v1.commonapp.models.sub_module import SubModule
from v1.commonapp.models.products import Product
from v1.commonapp.models.lifecycle import LifeCycle
from v1.commonapp.models.transition_configuration import TransitionConfiguration
from v1.commonapp.models.frequency import Frequency
from v1.commonapp.models.channel import Channel
from v1.commonapp.models.global_lookup import Global_Lookup
from v1.commonapp.models.division import Division
from v1.commonapp.models.notification_type import NotificationType
from v1.commonapp.models.notification_subtype import NotificationSubType

admin.site.register(Region)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Module)
admin.site.register(SubModule)
admin.site.register(Zone)
admin.site.register(Area)
admin.site.register(SubArea)
admin.site.register(Department)
admin.site.register(FormFactor)
admin.site.register(Notes)
admin.site.register(Document)
admin.site.register(ServiceType)
admin.site.register(ServiceSubTypes)
admin.site.register(DocumentType)
admin.site.register(DocumentSubType)
admin.site.register(Skills)
admin.site.register(StateConfiguration)
admin.site.register(TransitionConfiguration)
admin.site.register(EmailConfiguration)
admin.site.register(NotificationTemplate)
admin.site.register(Product)
admin.site.register(Notification)
admin.site.register(LifeCycle)
admin.site.register(AuditLog)
admin.site.register(Currency)
admin.site.register(Premise)
admin.site.register(Frequency)
admin.site.register(Channel)
admin.site.register(Global_Lookup)
admin.site.register(DepartmentSubtype)
admin.site.register(Division)
admin.site.register(NotificationType)
admin.site.register(NotificationSubType)
