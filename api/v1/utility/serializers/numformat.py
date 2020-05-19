__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat as UtilityServiceNumberFormatTbl


class UtilityServiceNumberFormatSerializer(serializers.ModelSerializer):
    item = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = UtilityServiceNumberFormatTbl
        fields = ('item',)

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            numformat_obj = super(UtilityServiceNumberFormatSerializer, self).update(instance, validated_data)
            numformat_obj.updated_by = user.id
            numformat_obj.updated_date = timezone.now()
            numformat_obj.currentno = numformat_obj.currentno + 1
            numformat_obj.save()
            return numformat_obj