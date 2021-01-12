from rest_framework import serializers, status
from django.db import transaction
from v1.utility.views.common_functions import set_working_hours_validated_data
from datetime import datetime
from v1.utility.models.utility_working_hours import UtilityWorkingHours as UtilityWorkingHoursTbl


class WorkingHourViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = UtilityWorkingHoursTbl
        fields = ('id_string', 'utility', 'utility_id_string', 'tenant', 'tenant_id_string')


class WorkingHourSerializer(serializers.ModelSerializer):
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UtilityWorkingHoursTbl
        fields = ('id_string', 'utility_id', 'tenant_id','mon_start', 'mon_end','tue_start','tue_end',
                  'wed_start', 'wed_end', 'thu_start','thu_end','fri_start','fri_end','sat_start','sat_end')

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_working_hours_validated_data(validated_data)
            working_hour_obj = super(WorkingHourSerializer, self).create(validated_data)
            working_hour_obj.created_by = user.id
            working_hour_obj.updated_by = user.id
            working_hour_obj.save()
            return working_hour_obj

    def update(self, instance, validated_data, user):
        validated_data = set_working_hours_validated_data(validated_data)
        with transaction.atomic():
            working_hour_obj = super(WorkingHourSerializer, self).update(instance, validated_data)
            working_hour_obj.tenant = user.tenant
            working_hour_obj.updated_by = user.id
            working_hour_obj.updated_date = datetime.utcnow()
            working_hour_obj.save()
            return working_hour_obj


class WorkingHourListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityWorkingHoursTbl
        fields = '__all__'
