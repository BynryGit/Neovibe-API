from api.messages import COSUMER_CONSENT_ALREADY_EXIST
from v1.consumer.views.common_functions import set_consumer_subcategory_validated_data
from rest_framework import status
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string,ConsumerCategory as ConsumerConsentTbl
from v1.registration.serializers.registration_type import RegistrationTypeListSerializer
from v1.registration.serializers.registration_subtype import RegistrationSubTypeListSerializer
from v1.consumer.models.consumer_consent import ConsumerConsent as ConsumerConsentTbl
from rest_framework import serializers
from v1.commonapp.views.custom_exception import CustomAPIException
from django.db import transaction
from datetime import datetime
from v1.consumer.views.common_functions import set_consumer_consent_validated_data

class ConsumerConsentListSerializer(serializers.ModelSerializer):
    registration_type = RegistrationTypeListSerializer(many="False", source='get_registration_type')
    registration_subtype = RegistrationSubTypeListSerializer(many="False", source='get_registration_subtype')
    class Meta:
        model = ConsumerConsentTbl
        fields = ('name', 'id_string','registration_type','registration_subtype','created_date','is_active','created_by')

class ConsumerConsentViewSerializer(serializers.ModelSerializer):
    

    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    

    

    class Meta:
        model = ConsumerConsentTbl
        fields = ('__all__')

class ConsumerConsentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)
    registration_type_id = serializers.CharField(required=True, max_length=200)
    registration_subtype_id = serializers.CharField(required=True, max_length=200) 
    

    class Meta:
        model = ConsumerConsentTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_consumer_consent_validated_data(validated_data)
            if ConsumerConsentTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                       utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(COSUMER_CONSENT_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                consumer_consent_obj = super(ConsumerConsentSerializer, self).create(validated_data)
                consumer_consent_obj.created_by = user.id
                consumer_consent_obj.updated_by = user.id
                consumer_consent_obj.save()
                return consumer_consent_obj

    def update(self, instance, validated_data, user):
        validated_data = set_consumer_consent_validated_data(validated_data)
        with transaction.atomic():
            consumer_consent_obj = super(ConsumerConsentSerializer, self).update(instance, validated_data)
            consumer_consent_obj.updated_by = user.id
            consumer_consent_obj.updated_date = datetime.utcnow()
            consumer_consent_obj.save()
            return consumer_consent_obj