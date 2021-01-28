from rest_framework import serializers
from v1.utility.models.utility_document_type import UtilityDocumentType as UtilityDocumentTypeTbl


class UtilityDocumentTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityDocumentTypeTbl
        fields = ('name', 'id_string','document_size', 'is_active','created_by','created_date')