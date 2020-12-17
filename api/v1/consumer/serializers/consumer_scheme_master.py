from datetime import datetime

from django.db import transaction
from rest_framework import serializers
from v1.consumer.models.consumer_scheme_master import ConsumerSchemeMaster
from v1.consumer.views.common_functions import set_scheme_validated_data


class ConsumerSchemeMasterListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsumerSchemeMaster
        fields = ('scheme_name', 'id_string')


class ConsumerSchemeMasterViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ConsumerSchemeMaster
        fields = ('id_string', 'scheme_name', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string')


class ConsumerSchemeMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsumerSchemeMaster
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data = set_scheme_validated_data(validated_data)
        with transaction.atomic():
            scheme = super(ConsumerSchemeMasterSerializer, self).create(validated_data)
            scheme.created_by = user.id
            scheme.created_date = datetime.utcnow()
            scheme.tenant = user.tenant
            scheme.utility = user.utility
            scheme.save()
        return scheme

    def update(self, instance, validated_data, user):
        validated_data = set_scheme_validated_data(validated_data)
        with transaction.atomic():
            scheme = super(ConsumerSchemeMasterSerializer, self).update(instance, validated_data)
            scheme.updated_by = user.id
            scheme.updated_date = datetime.utcnow()
            scheme.save()
        return scheme