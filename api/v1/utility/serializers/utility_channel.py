from rest_framework import serializers, status
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.utility.models.utility_channel import UtilityChannel as UtilityChannelTbl


class UtilityChannelListSerializer(serializers.ModelSerializer):
    utility = serializers.ReadOnlyField(source='utility.name')
    class Meta:
        model = UtilityChannelTbl
        fields = ('utility','name', 'id_string','is_active','created_by','created_date')