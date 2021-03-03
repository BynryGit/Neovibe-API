from rest_framework import serializers
from v1.commonapp.models.document import Document as DocumentTbl
from rest_framework import serializers, status
from v1.commonapp.serializers.document_type import DocumentTypeListSerializer
from api.messages import DOCUMENT_ALREADY_EXIST
from datetime import datetime
from django.db import transaction
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.common_functions import set_document_validated_data


class DocumentShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTbl
        fields = ('id_string', 'document_name')


class DocumentViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = DocumentTbl
        fields = (
            'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'document_name', 'id_string')


class DocumentSerializer(serializers.ModelSerializer):
    document_name = serializers.CharField(required=True, max_length=200,
                                          error_messages={"required": "The field document name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    document_type_id = serializers.CharField(required=False, max_length=200)
    module_id = serializers.CharField(required=False, max_length=200)
    sub_module_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = DocumentTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_document_validated_data(validated_data)
            if DocumentTbl.objects.filter(document_name=validated_data['document_name'], tenant_id=validated_data['tenant_id'],
                                          utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(DOCUMENT_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                document_obj = super(DocumentSerializer, self).create(validated_data)
                document_obj.created_by = user.id
                document_obj.updated_by = user.id
                document_obj.save()
                return document_obj

    def update(self, instance, validated_data, user):
        validated_data = set_document_validated_data(validated_data)
        with transaction.atomic():
            document_obj = super(DocumentSerializer, self).update(instance, validated_data)
            document_obj.updated_by = user.id
            document_obj.updated_date = datetime.utcnow()
            document_obj.save()
            return document_obj


class DocumentListSerializer(serializers.ModelSerializer):
    document_type = DocumentTypeListSerializer(source="get_utility_document_type")

    class Meta:
        model = DocumentTbl
        fields = ('document_name', 'id_string', 'document_type', 'document_size', 'is_active', 'created_by', 'created_date')