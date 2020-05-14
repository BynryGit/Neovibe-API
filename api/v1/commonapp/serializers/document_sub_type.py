__author__ = "Arpita"

from rest_framework import serializers

from v1.commonapp.models.document_sub_type import DocumentSubType


class DocumentSubTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentSubType
        fields = ('name', 'id_string')