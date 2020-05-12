from rest_framework import serializers

from v1.commonapp.models.form_factor import FormFactor


class FormFactorListSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = FormFactor
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'is_active')


class FormFactorViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = FormFactor
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'is_active')