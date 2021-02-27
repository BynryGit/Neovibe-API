
from rest_framework import serializers, status
from v1.commonapp.models.notification_subtype import NotificationSubType as NotificationSubTypeTbl
from v1.commonapp.serializers.notification_type import NotificationTypeListSerializer
from v1.commonapp.common_functions import set_notification_subtype_validated_data
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import NOTIFICATION_SUBTYPE_ALREADY_EXIST
from datetime import datetime
from django.db import transaction


class NotificationSubTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = NotificationSubTypeTbl
        fields = (
            'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'id_string')


class NotificationSubTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    notification_type_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = NotificationSubTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_notification_subtype_validated_data(validated_data)
            if NotificationSubTypeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                                     utility_id=validated_data['utility_id'],notification_type_id=validated_data['notification_type_id']).exists():
                raise CustomAPIException(NOTIFICATION_SUBTYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                notification_subtype_obj = super(NotificationSubTypeSerializer, self).create(validated_data)
                notification_subtype_obj.created_by = user.id
                notification_subtype_obj.save()
                return notification_subtype_obj

    def update(self, instance, validated_data, user):
        validated_data = set_notification_subtype_validated_data(validated_data)
        with transaction.atomic():
            notification_subtype_obj = super(NotificationSubTypeSerializer, self).update(instance, validated_data)
            notification_subtype_obj.updated_by = user.id
            notification_subtype_obj.updated_date = datetime.utcnow()
            notification_subtype_obj.save()
            return notification_subtype_obj


class NotificationSubTypeListSerializer(serializers.ModelSerializer):
    notification_type = NotificationTypeListSerializer(source="get_notification_type")
    is_active = serializers.SerializerMethodField(method_name='conversion_bool')

    class Meta:
        model = NotificationSubTypeTbl
        fields = ('name', 'id_string', 'notification_type', 'created_date', 'is_active', 'created_by')

    def conversion_bool(self, instance):
        if instance.is_active == True:
            return "Yes"
        else:
            return "No"