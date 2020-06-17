__author__ = "Arpita"
from django.db import transaction
from datetime import datetime

from rest_framework import serializers, status

from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.userapp.models.user_bank import UserBank
from v1.userapp.models.user_bank_detail import UserBankDetail
from v1.utility.serializers.utility import UtilitySerializer


class GetUserBankSerializer(serializers.ModelSerializer):

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    area = GetBankSerializer(many=False, required=True, source='get_area')

    class Meta:
        model = UserBank
        fields = ('id_string', 'area')


class UserBankViewSerializer(serializers.ModelSerializer):

    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = UserBank
        fields = ('id_string', 'tenant', 'created_date')


class UserBankSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(required=False, max_length=200)
    area_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UserBank
        fields = '__all__'

    def create(self, validate_data, user):
        validated_data = set_user_bank_validated_data(validate_data)
        if UserBank.objects.filter(user_id=validated_data['user_id'], bank_id=validated_data['bank_id'],
                                   tenant=user.tenant, is_active=True).exists():
            raise CustomAPIException("Bank already exists for specified user!",
                                     status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                user_area_obj = super(UserBankSerializer, self).create(validated_data)
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
            user_area_obj = super(UserBankSerializer, self).update(instance, validated_data)
            user_area_obj.updated_by = user.id
            user_area_obj.updated_date = datetime.utcnow()
            user_area_obj.is_active = True
            user_area_obj.save()
            return user_area_obj


