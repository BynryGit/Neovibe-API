__author__ = "Arpita"

from rest_framework import serializers

from v1.commonapp.models.document_type import DocumentType


class DocumentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentType
        fields = ('name', 'id_string')
