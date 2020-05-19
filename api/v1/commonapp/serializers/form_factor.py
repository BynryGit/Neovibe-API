__author__ = "Arpita"

from rest_framework import serializers

from v1.commonapp.models.form_factor import FormFactor
from v1.tenant.serializers.tenant import TenantSerializer
from v1.utility.serializers.utility import UtilitySerializer


class FormFactorSerializer(serializers.ModelSerializer):

    class Meta:
        model = FormFactor
        fields = ('name', 'id_string')


class FormFactorListSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = FormFactor
        fields = ('id_string', 'tenant', 'utility', 'name', 'is_active')


class FormFactorViewSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = FormFactor
        fields = ('id_string', 'tenant', 'utility', 'name', 'is_active')