from django.db import transaction
from datetime import datetime

from rest_framework import serializers, status

from api.settings import DISPLAY_DATE_TIME_FORMAT

from v1.commonapp.serializers.area import GetAreaSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.serializers.tenant import GetTenantSerializer
from v1.userapp.models.user_area import UserArea
from v1.userapp.views.common_functions import set_user_area_validated_data


class GetUserAreaSerializer(serializers.ModelSerializer):

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    area = GetAreaSerializer(many=False, required=True, source='get_area')

    class Meta:
        model = UserArea
        fields = ('id_string', 'area')


class UserAreaViewSerializer(serializers.ModelSerializer):

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = UserArea
        fields = ('id_string', 'tenant', 'created_date')


class UserAreaSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=False, max_length=200)
    area_id = serializers.CharField(required=False, max_length=200)
    is_active = serializers.BooleanField(required=False)

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
                user_area_obj.created_date = datetime.utcnow()
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


