from rest_framework import serializers, status
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.commonapp.models.notification_template import NotificationTemplate as NotificationTemplateTbl
from datetime import datetime
from django.db import transaction
from api.messages import NOTIFICATION_TEMPLATE_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.common_functions import set_notification_template_validated_data
from v1.commonapp.serializers.sub_module import SubModuleListSerializer


class NotificationTemplateViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = NotificationTemplateTbl
        fields = (
            'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'template', 'id_string')


class NotificationTemplateSerializer(serializers.ModelSerializer):
    template = serializers.CharField(required=True, max_length=1000,
                                     error_messages={"required": "The field Template is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)


    class Meta:
        model = NotificationTemplateTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_notification_template_validated_data(validated_data)
            if NotificationTemplateTbl.objects.filter(template=validated_data['template'],
                                                      tenant_id=validated_data['tenant_id'],
                                                      utility_id=validated_data['utility_id'],
                                                      ).exists():
                raise CustomAPIException(NOTIFICATION_TEMPLATE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                notification_template_obj = super(NotificationTemplateSerializer, self).create(validated_data)
                notification_template_obj.created_by = user.id
                notification_template_obj.save()
                return notification_template_obj

    def update(self, instance, validated_data, user):
        validated_data = set_notification_template_validated_data(validated_data)
        if NotificationTemplateTbl.objects.filter(template=validated_data['template'],
                                                  tenant_id=validated_data['tenant_id'],
                                                  utility_id=validated_data['utility_id'],
                                                  ).exists():
            raise CustomAPIException(NOTIFICATION_TEMPLATE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                notification_template_obj = super(NotificationTemplateSerializer, self).update(instance, validated_data)
                notification_template_obj.updated_by = user.id
                notification_template_obj.updated_date = datetime.utcnow()
                notification_template_obj.save()
                return notification_template_obj


class NotificationTemplateListSerializer(serializers.ModelSerializer):
    sub_module = SubModuleListSerializer(source='get_sub_module')

    class Meta:
        model = NotificationTemplateTbl
        fields = ('template', 'id_string', 'sub_module')
