from rest_framework import serializers
from v1.utility.models.contact_us import ContactUs


class ContactUsListSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = ContactUs
        fields = ('tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'email', "emergency_no",
                  "working_days", "portal_site")
