from rest_framework import serializers, status
from django.db import transaction
from datetime import datetime
from api.messages import READ_CYCLE_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.serializers.city import CityListSerializer
from v1.commonapp.serializers.zone import ZoneListSerializer
from v1.commonapp.serializers.division import DivisionListSerializer
from v1.commonapp.serializers.area import AreaListSerializer
from v1.commonapp.serializers.sub_area import SubAreaListSerializer
from v1.billing.models.bill_cycle import BillCycle as BillCycleTbl

class BillCycleShortViewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BillCycleTbl
        fields = ('id_string', 'bill_cycle_name','bill_cycle_code')

class BillCycleListSerializer(serializers.ModelSerializer):
    city = CityListSerializer(source="get_city")
    zone = ZoneListSerializer(source="get_zone")
    area = AreaListSerializer(source="get_area")

    class Meta:
        model = BillCycleTbl
        fields = ('id_string', 'bill_cycle_name','bill_cycle_code','city','zone','area')