__author__ = "Aki"

from rest_framework import serializers
from v1.commonapp.models.notes import Notes as NotesTbl
from v1.tenant.serializers.tenant import TenantMasterSerializer
from v1.utility.serializers.utility import UtilitySerializer


class NoteSerializer(serializers.ModelSerializer):
    tenant = TenantMasterSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = NotesTbl
        fields = ('id_string', 'tenant', 'utility', 'note_name', 'note_color', 'note', 'status',
                  'is_active', 'created_by', 'created_date')

    def create(self, validated_data, user):
        note = super(NoteSerializer, self).create(validated_data)
        note.created_by = user
        note.save()
        return note