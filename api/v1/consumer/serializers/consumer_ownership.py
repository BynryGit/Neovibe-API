from rest_framework import serializers
from v1.consumer.models.consumer_ownership import ConsumerOwnership as ConsumerOwnershipTbl
from api.settings.prod import DISPLAY_DATE_TIME_FORMAT
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import COSUMER_OWNERSHIP_ALREADY_EXIST
from rest_framework import status

from v1.consumer.views.common_functions import set_consumer_ownership_validated_data


class ConsumerOwnershipListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerOwnershipTbl
        fields = ('name', 'id_string', 'created_by', 'created_date', 'is_active')


class ConsumerOwnershipViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ConsumerOwnershipTbl
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string')


class ConsumerOwnershipSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = ConsumerOwnershipTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_consumer_ownership_validated_data(validated_data)
            if ConsumerOwnershipTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                                   utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(COSUMER_OWNERSHIP_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                consumer_ownership_obj = super(ConsumerOwnershipSerializer, self).create(validated_data)
                consumer_ownership_obj.created_by = user.id
                consumer_ownership_obj.updated_by = user.id
                consumer_ownership_obj.save()
                return consumer_ownership_obj

    def update(self, instance, validated_data, user):
        validated_data = set_consumer_ownership_validated_data(validated_data)
        with transaction.atomic():
            consumer_ownership_obj = super(ConsumerOwnershipSerializer, self).update(instance, validated_data)
            consumer_ownership_obj.updated_by = user.id
            consumer_ownership_obj.updated_date = datetime.utcnow()
            consumer_ownership_obj.save()
            return consumer_ownership_obj
