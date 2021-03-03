
from rest_framework import serializers, status
from v1.commonapp.models.notification_type import NotificationType as NotificationTypeTbl
from v1.commonapp.common_functions import set_notification_type_validated_data
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import NOTIFICATION_TYPE_ALREADY_EXIST
from datetime import datetime
from django.db import transaction


class NotificationTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = NotificationTypeTbl
        fields = (
            'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'id_string')


class NotificationTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)


    class Meta:
        model = NotificationTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_notification_type_validated_data(validated_data)
            if NotificationTypeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                                  utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(NOTIFICATION_TYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                notification_type_obj = super(NotificationTypeSerializer, self).create(validated_data)
                notification_type_obj.created_by = user.id
                notification_type_obj.save()
                return notification_type_obj

    def update(self, instance, validated_data, user):
        validated_data = set_notification_type_validated_data(validated_data)
        with transaction.atomic():
            notification_type_obj = super(NotificationTypeSerializer, self).update(instance, validated_data)
            notification_type_obj.updated_by = user.id
            notification_type_obj.updated_date = datetime.utcnow()
            notification_type_obj.save()
            return notification_type_obj


class NotificationTypeListSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField(method_name='conversion_bool')

    class Meta:
        model = NotificationTypeTbl
        fields = ('name', 'id_string', 'created_date', 'is_active', 'created_by')

    def conversion_bool(self, instance):
        if instance.is_active == True:
            return "Yes"
        else:
            return "No"
