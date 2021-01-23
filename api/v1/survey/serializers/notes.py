__author__ = "priyanka"

from rest_framework import serializers
from v1.commonapp.models.notes import Notes as NotesTbl
from v1.tenant.serializers.tenant import TenantSerializer
from v1.utility.serializers.utility import UtilitySerializer
from api.settings.prod import DISPLAY_DATE_TIME_FORMAT

class NoteSerializer(serializers.ModelSerializer):
    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = NotesTbl
        fields = ('id_string', 'tenant', 'utility', 'note_name', 'note_color', 'note', 'status',
                  'is_active', 'created_by', 'created_date')

    def create(self, validated_data, user):
        note = super(NoteSerializer, self).create(validated_data)
        note.created_by = user
        note.save()
        return note