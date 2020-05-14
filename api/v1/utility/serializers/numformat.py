__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat as UtilityServiceNumberFormatTbl


class NumformatSerializer(serializers.ModelSerializer):
    utility = serializers.ReadOnlyField(source='utility')
    currentnumber = serializers.SerializerMethodField()

    def get_currentnumber(self, numformat_obj):
        if numformat_obj.prefix:
            currentnumber = str(numformat_obj.prefix) + numformat_obj.currentno
        else:
            currentnumber = str(numformat_obj.currentno)
        return currentnumber

    class Meta:
        model = UtilityServiceNumberFormatTbl
        fields = ('utility', 'currentnumber', 'is_active')

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            numformat_obj = super(NumformatSerializer, self).update(instance, validated_data)
            numformat_obj.updated_by = user
            numformat_obj.updated_date=timezone.now()
            numformat_obj.currentno = numformat_obj.currentno + 1
            numformat_obj.save()
            return numformat_obj