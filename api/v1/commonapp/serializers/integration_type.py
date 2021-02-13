from rest_framework import serializers
from v1.commonapp.models.integration_type import IntegrationType as IntegrationTypeTbl


class IntegrationTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationTypeTbl
        fields = ('name', 'id_string', 'is_active', 'created_by', 'created_date')



