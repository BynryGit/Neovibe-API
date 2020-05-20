__author__ = "Priyanka"

from rest_framework import serializers
from datetime import datetime
from django.db import transaction
from v1.asset.models.asset_master import Assset as AsssetTbl

class AssetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsssetTbl
        fields = ('__all__')