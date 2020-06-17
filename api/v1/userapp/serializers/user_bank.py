__author__ = "Arpita"
from django.db import transaction
from datetime import datetime

from rest_framework import serializers, status

from v1.commonapp.views.custom_exception import CustomAPIException
from v1.userapp.models.user_bank import UserBank

from v1.userapp.views.common_functions import set_user_bank_validated_data


class UserBankSerializer(serializers.ModelSerializer):
    utility_id = serializers.CharField(required=False, max_length=200)
    user_id = serializers.CharField(required=False, max_length=200)
    bank_id = serializers.CharField(required=False, max_length=200)

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
                user_bank_obj = super(UserBankSerializer, self).create(validated_data)
                user_bank_obj.created_by = user.id
                user_bank_obj.updated_by = user.id
                user_bank_obj.created_date = datetime.utcnow()
                user_bank_obj.updated_date = datetime.utcnow()
                user_bank_obj.tenant = user.tenant
                user_bank_obj.is_active = True
                user_bank_obj.save()
                return user_bank_obj

    def update(self, instance, validate_data, user):
        validated_data = set_user_bank_validated_data(validate_data)
        with transaction.atomic():
            user_bank_obj = super(UserBankSerializer, self).update(instance, validated_data)
            user_bank_obj.updated_by = user.id
            user_bank_obj.updated_date = datetime.utcnow()
            user_bank_obj.is_active = True
            user_bank_obj.save()
            return user_bank_obj


