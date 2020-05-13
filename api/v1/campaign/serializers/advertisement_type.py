from rest_framework import serializers
from v1.campaign.models.advertisement_type import AdvertisementType

class AdvertisementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementType
        fields = ('name','id_string')


class AdvertisementViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = AdvertisementType
        fields = ('id_string', 'name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string')