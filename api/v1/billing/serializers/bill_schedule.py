__author__ = "priyanka"

from django.db import transaction
from django.utils import timezone
from api.messages import DATA_ALREADY_EXISTS
from rest_framework import serializers, status
from v1.commonapp.common_functions import ChoiceField
from v1.commonapp.serializers.global_lookup import GlobalLookupShortViewSerializer
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.billing.models.bill_schedule import ScheduleBill as ScheduleBillTbl
from v1.billing.serializers.bill_cycle import BillCycleShortViewSerializer
from v1.billing.views.common_functions import set_schedule_bill_validated_data
from v1.utility.serializers.utility_product import UtilityProductShortViewSerializer
from v1.billing.views.common_functions import set_schedule_bill_validated_data
from datetime import datetime

class ScheduleBillShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleBillTbl
        fields = ('id_string','name')


class ScheduleBillViewSerializer(serializers.ModelSerializer):
    tenant = TenantMasterViewSerializer()
    utility = UtilityMasterViewSerializer()
    bill_cycle_id = BillCycleShortViewSerializer(many=False, source='get_bill_cycle_name')
    frequency_id = GlobalLookupShortViewSerializer(many=False, source='get_frequency_name')
    repeat_every_id = GlobalLookupShortViewSerializer(many=False, source='get_repeat_every_name')
    recurring_id = GlobalLookupShortViewSerializer(many=False, source='get_recurring_name')
    utility_product_id = UtilityProductShortViewSerializer(many=False, source='get_utility_product_name')
    schedule_status = ChoiceField(choices=ScheduleBillTbl.SCHEDULE_STATUS)

    class Meta:
        model = ScheduleBillTbl
        fields = ('id_string', 'name', 'description', 'schedule_status', 'start_date', 'end_date', 'created_date',
                  'updated_date', 'created_by', 'updated_by', 'recurring_id', 'repeat_every_id', 'bill_cycle_id',
                  'frequency_id', 'occurs_on', 'utility_product_id', 'tenant', 'utility')


class ScheduleBillSerializer(serializers.ModelSerializer):
    utility_id = serializers.UUIDField(required=True)
    bill_cycle_id = serializers.UUIDField(required=True)
    frequency_id = serializers.UUIDField(required=False)
    repeat_every_id = serializers.UUIDField(required=False)
    recurring_id = serializers.UUIDField(required=False)
    utility_product_id = serializers.UUIDField(required=False)
    occurs_on = serializers.JSONField(required=False)

    class Meta:
        model = ScheduleBillTbl
        fields = ('__all__')

    def create(self, validated_data, user):
        validated_data = set_schedule_bill_validated_data(validated_data)
        if ScheduleBillTbl.objects.filter(tenant=user.tenant, utility_id=validated_data['utility_id'],
                                      bill_cycle_id=validated_data["bill_cycle_id"],start_date__date=(validated_data['start_date']).date(), is_active=True).exists():
            raise CustomAPIException(DATA_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                schedule_obj = super(ScheduleBillSerializer, self).create(validated_data)
                schedule_obj.tenant = user.tenant
                schedule_obj.created_by = user.id
                schedule_obj.save()
                return schedule_obj

    def update(self, instance, validated_data, user):
        validated_data = set_schedule_bill_validated_data(validated_data)
        with transaction.atomic():
            schedule_obj = super(ScheduleBillSerializer, self).update(instance, validated_data)
            schedule_obj.tenant = user.tenant
            schedule_obj.updated_by = user.id
            schedule_obj.updated_date = timezone.now()
            schedule_obj.save()
            return schedule_obj
