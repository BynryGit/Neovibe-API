from rest_framework import serializers, status
from v1.payment.models.payment_type import PaymentType as PaymentTypeTbl
from django.db import transaction
from v1.payment.views.common_functions import set_payment_type_validated_data
from datetime import datetime
from api.messages import PAYMENT_TYPE_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.utility.models.utility_payment_type import UtilityPaymentType as UtilityPaymentTypeTbl


class PaymentTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTypeTbl
        fields = ('name', 'key', 'id_string', 'is_active', 'created_by', 'created_date')


class PaymentTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = UtilityPaymentTypeTbl
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string')


class PaymentTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)

    payment_type_id = serializers.CharField(required=False, max_length=200)


    class Meta:
        model = UtilityPaymentTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_payment_type_validated_data(validated_data)
            if UtilityPaymentTypeTbl.objects.filter(tenant_id=validated_data['tenant_id'],
                                                    utility_id=validated_data['utility_id'],name=validated_data['name']).exists():
                raise CustomAPIException(PAYMENT_TYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:

                payment_type_obj = super(PaymentTypeSerializer, self).create(validated_data)
                payment_type_obj.created_by = user.id
                payment_type_obj.created_date = datetime.utcnow()
                payment_type_obj.save()
                return payment_type_obj

    def update(self, instance, validated_data, user):
        validated_data = set_payment_type_validated_data(validated_data)
        with transaction.atomic():
            payment_type_obj = super(PaymentTypeSerializer, self).update(instance, validated_data)
            payment_type_obj.tenant = user.tenant
            payment_type_obj.updated_by = user.id
            payment_type_obj.updated_date = datetime.utcnow()
            payment_type_obj.save()
            return payment_type_obj
