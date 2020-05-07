from django.contrib import admin
from v1.survey.models.survey import Survey
from v1.survey.models.survey_objective import SurveyObjective
from v1.survey.models.survey_status import SurveyStatus
from v1.survey.models.survey_type import SurveyType
from v1.survey.models.survey_consumer import SurveyConsumer
from v1.survey.models.survey_assignment import SurveyAssignment
from v1.survey.models.survey_transaction_status import SurveyTransactionStatus

admin.site.register(Survey)
admin.site.register(SurveyObjective)
admin.site.register(SurveyStatus)
admin.site.register(SurveyType)
admin.site.register(SurveyConsumer)
admin.site.register(SurveyAssignment)
admin.site.register(SurveyTransactionStatus)
