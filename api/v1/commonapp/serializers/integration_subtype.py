from rest_framework import serializers
from v1.commonapp.models.integration_subtype import IntegrationSubType as IntegrationSubTypeTbl
from v1.commonapp.serializers.integration_type import IntegrationTypeListSerializer


class IntegrationSubTypeListSerializer(serializers.ModelSerializer):
    integration_type = IntegrationTypeListSerializer(source='get_integration_type')

    class Meta:
        model = IntegrationSubTypeTbl
        fields = ('name', 'id_string', 'integration_type', 'is_active', 'created_by', 'created_date')
