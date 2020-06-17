from django.db import transaction
from datetime import datetime

from rest_framework import serializers, status

from api.settings import DISPLAY_DATE_TIME_FORMAT

from v1.commonapp.serializers.area import GetAreaSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.userapp.models.user_area import UserArea
from v1.userapp.views.common_functions import set_user_area_validated_data


class GetUserAreaSerializer(serializers.ModelSerializer):

    area = GetAreaSerializer(many=False, required=True, source='get_area')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = UserArea
        fields = ('id_string', 'area', 'created_date', 'updated_date')


class UserAreaViewSerializer(serializers.ModelSerializer):

    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    created_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)
    updated_date = serializers.DateTimeField(format=DISPLAY_DATE_TIME_FORMAT, read_only=True)

    class Meta:
        model = UserArea
        fields = ('id_string', 'tenant', 'created_date', 'updated_date')


class UserAreaSerializer(serializers.ModelSerializer):
    utility_id = serializers.CharField(required=False, max_length=200)
    user_id = serializers.CharField(required=False, max_length=200)
    area_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UserArea
        fields = '__all__'

    def create(self, validate_data, user):
        validated_data = set_user_area_validated_data(validate_data)
        if UserArea.objects.filter(user_id=validated_data['user_id'], area_id=validated_data['area_id'],
                                   tenant=user.tenant, is_active=True).exists():
            raise CustomAPIException("Area already exists for specified user!",
                                     status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                user_area_obj = super(UserAreaSerializer, self).create(validated_data)
                user_area_obj.created_by = user.id
                user_area_obj.updated_by = user.id
                user_area_obj.created_date = datetime.utcnow()
                user_area_obj.updated_date = datetime.utcnow()
                user_area_obj.tenant = user.tenant
                user_area_obj.is_active = True
                user_area_obj.save()
                return user_area_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            user_area_obj = super(UserAreaSerializer, self).update(instance, validated_data)
            user_area_obj.updated_by = user.id
            user_area_obj.updated_date = datetime.utcnow()
            user_area_obj.is_active = True
            user_area_obj.save()
            return user_area_obj


