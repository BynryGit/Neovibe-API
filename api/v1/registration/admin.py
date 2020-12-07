from django.contrib import admin
from v1.registration.models.registration_status import RegistrationStatus
from v1.registration.models.registration_type import RegistrationType
from v1.registration.models.registrations import Registration
from v1.registration.models.registration_subtype import RegistrationSubType
admin.site.register(RegistrationStatus)
admin.site.register(RegistrationType)
admin.site.register(RegistrationSubType)
admin.site.register(Registration)
