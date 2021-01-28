__author__ = "Arpita"


from rest_framework import serializers, status
from django.db import transaction
from v1.commonapp.common_functions import set_document_subtype_validated_data
from datetime import datetime
from api.messages import DOCUMENT_SUBTYPE_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.models.document_sub_type import DocumentSubType as DocumentSubTypeTbl
from v1.utility.serializers.utility_document_type import UtilityDocumentTypeListSerializer


class DocumentSubTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = DocumentSubTypeTbl
        fields = '__all__'


class DocumentSubTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    document_type_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = DocumentSubTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_document_subtype_validated_data(validated_data)
            if DocumentSubTypeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                                 utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(DOCUMENT_SUBTYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:

                document_subtype_obj = super(DocumentSubTypeSerializer, self).create(validated_data)
                document_subtype_obj.created_by = user.id
                document_subtype_obj.updated_by = user.id
                document_subtype_obj.save()
                return document_subtype_obj

    def update(self, instance, validated_data, user):
        validated_data = set_document_subtype_validated_data(validated_data)
        with transaction.atomic():
            document_subtype_obj = super(DocumentSubTypeSerializer, self).update(instance, validated_data)
            document_subtype_obj.tenant = user.tenant
            document_subtype_obj.updated_by = user.id
            document_subtype_obj.updated_date = datetime.utcnow()
            document_subtype_obj.save()
            return document_subtype_obj


class DocumentSubTypeListSerializer(serializers.ModelSerializer):
    document_type = UtilityDocumentTypeListSerializer(source="get_utility_document_type")

    class Meta:
        model = DocumentSubTypeTbl
        fields = ('name', 'id_string', 'document_type', 'created_date', 'created_by')
