from rest_framework import serializers, status
from django.db import transaction
from v1.meter_data_management.views.common_function import set_reader_status_validated_data
from datetime import datetime
from api.messages import READER_STATUS_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.meter_data_management.models.reader_status import ReaderStatus as ReaderStatusTbl
from v1.commonapp.serializers.meter_status import MeterStatusListSerializer


class ReaderStatusViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ReaderStatusTbl
        fields = ('name', 'id_string', 'utility', 'utility_id_string', 'tenant', 'tenant_id_string')


class ReaderStatusSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    meter_status_id = serializers.CharField(required=False, max_length=200)
    status_code = serializers.CharField(required=False,max_length=200)
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = ReaderStatusTbl
        fields = ('name', 'id_string', 'status_code', 'meter_status_id', 'utility_id', 'tenant_id')

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_reader_status_validated_data(validated_data)
            if ReaderStatusTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                              utility_id=validated_data['utility_id'], status_code=validated_data['status_code'],meter_status_id=validated_data['meter_status_id']).exists():
                raise CustomAPIException(READER_STATUS_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                reader_status_obj = super(ReaderStatusSerializer, self).create(validated_data)
                reader_status_obj.created_by = user.id
                reader_status_obj.save()
                return reader_status_obj

    def update(self, instance, validated_data, user):
        validated_data = set_reader_status_validated_data(validated_data)
        if ReaderStatusTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                          utility_id=validated_data['utility_id'], status_code=validated_data['status_code'],meter_status_id=validated_data['meter_status_id']).exists():
            raise CustomAPIException(READER_STATUS_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                reader_status_obj = super(ReaderStatusSerializer, self).update(instance, validated_data)
                reader_status_obj.tenant = user.tenant
                reader_status_obj.updated_by = user.id
                reader_status_obj.updated_date = datetime.utcnow()
                reader_status_obj.save()
                return reader_status_obj


class ReaderStatusListSerializer(serializers.ModelSerializer):
    meter_status = MeterStatusListSerializer(source='get_meter_status')

    class Meta:
        model = ReaderStatusTbl
        fields = ('name', 'id_string', 'status_code', 'meter_status', 'created_date', 'is_active', 'created_by')
