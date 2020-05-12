__author__ = "Priyanka"

from django.db import transaction
from rest_framework import serializers
from v1.campaign.models.campaign import Campaign as CampaignTbl


class CampaignViewSerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = CampaignTbl
        fields = ('id_string', 'tenant_name', 'group_id', 'name', 'objective_id', 'description',
                  'frequency_id','potential_consumers','actual_consumers','budget_amount','actual_amount','category_id',
                  'sub_category_id','start_date','end_date','area_id','sub_area_id','status_id','is_active')

