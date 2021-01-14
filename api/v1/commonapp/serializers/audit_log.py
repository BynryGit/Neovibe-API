from rest_framework import serializers
from v1.commonapp.models.audit_log import AuditLog


class AuditLogViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = AuditLog
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'created_date',
                  'field_name', 'old_value', 'new_value', 'remark', 'log_date')
