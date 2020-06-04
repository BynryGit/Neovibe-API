__author__ = "Arpita"
from django.db import transaction
from datetime import datetime

from rest_framework import serializers, status

from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.serializers.tenant import GetTenantSerializer
from v1.userapp.models.user_bank_detail import UserBankDetail
from v1.utility.serializers.utility import UtilitySerializer


class UserBankListSerializer(serializers.ModelSerializer):
    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = UserBankDetail
        fields = ('id_string', 'tenant', 'utility', 'bank_name', 'branch_name', 'branch_city', 'account_number',
                  'account_type', 'account_name', 'ifsc_no', 'pan_no', 'gst_no', 'tax_id_no', 'is_active', 'created_by',
                  'created_date')


class GetUserBankSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserBankDetail
        fields = ('id_string', 'bank_name')


class UserBankViewSerializer(serializers.ModelSerializer):
    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = UserBankDetail
        fields = ('id_string', 'bank_name', 'branch_name', 'branch_city', 'account_number', 'account_type', 'account_name',
                  'ifsc_no', 'pan_no', 'gst_no', 'tax_id_no', 'is_active', 'created_date')


class UserBankSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(required=False, max_length=200)
    branch_name = serializers.CharField(required=False, max_length=200)
    branch_city = serializers.CharField(required=False, max_length=200)
    account_number = serializers.CharField(required=False, max_length=200)
    account_type = serializers.CharField(required=False, max_length=200)
    account_name = serializers.CharField(required=False, max_length=200)
    ifsc_no = serializers.CharField(required=False, max_length=200)
    pan_no = serializers.CharField(required=False, max_length=200)
    gst_no = serializers.CharField(required=False, max_length=200)
    tax_id_no = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UserBankDetail
        fields = '__all__'

    def create(self, validated_data, user):
        if UserBankDetail.objects.filter(bank_name=validated_data['bank_name'], branch_name=validated_data['branch_name'], branch_city=validated_data['branch_city'], tenant=user.tenant, is_active=True).exists():
            raise CustomAPIException("Role already exists!", status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                user_bank_obj = super(UserBankSerializer, self).create(validated_data)
                user_bank_obj.created_by = user.id
                user_bank_obj.created_date = datetime.utcnow()
                user_bank_obj.tenant = user.tenant
                user_bank_obj.utility = user.utility
                user_bank_obj.is_active = True
                user_bank_obj.save()
                return user_bank_obj

    def update(self, instance, validated_data, user):
        if UserBankDetail.objects.exclude(id_string=instance.id_string).filter(bank_name=validated_data['bank_name'], branch_name=validated_data['branch_name'], branch_city=validated_data['branch_city'], tenant=user.tenant, is_active=True).exists():
            raise CustomAPIException("Role already exists!", status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                user_bank_obj = super(UserBankSerializer, self).update(instance, validated_data)
                user_bank_obj.updated_by = user.id
                user_bank_obj.updated_date = datetime.utcnow()
                user_bank_obj.is_active = True
                user_bank_obj.save()
                return user_bank_obj
