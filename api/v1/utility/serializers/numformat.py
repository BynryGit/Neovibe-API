
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers, status
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat as UtilityServiceNumberFormatTbl
from datetime import datetime
from v1.utility.views.common_functions import set_numformat_validated_data, generate_current_no
from v1.utility.serializers.utility_sub_module import UtilitySubModuleViewSerializer,UtilitySubModuleListSerializer
from v1.commonapp.serializers.sub_module import SubModuleShortViewSerializer
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import NUMFORMAT_ALREADY_EXIST

class UtilityServiceNumberFormatSerializer(serializers.ModelSerializer):
    sub_module_id = serializers.CharField(required=True, max_length=200)
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    prefix = serializers.CharField(required=False, max_length=200)
    startingno = serializers.CharField(required=False, max_length=200)
    currentno = serializers.CharField(required=False, max_length=200)
    

    class Meta:
        model = UtilityServiceNumberFormatTbl
        fields = ('sub_module_id','utility_id','tenant_id','prefix','startingno','currentno')
    
  
    
    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_numformat_validated_data(validated_data)
            if UtilityServiceNumberFormatTbl.objects.filter(tenant_id=validated_data['tenant_id'],
                                        utility_id=validated_data['utility_id'],prefix=validated_data['prefix'],startingno=validated_data['startingno'],currentno=validated_data['currentno']).exists():
                raise CustomAPIException(NUMFORMAT_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                numformat_obj = super(UtilityServiceNumberFormatSerializer, self).create(validated_data)
                numformat_obj.created_by = user.id
                numformat_obj.updated_by = user.id
                numformat_obj.tenant = user.tenant
                numformat_obj.is_active = True
                numformat_obj.save()
                return numformat_obj

    def update(self, instance, validated_data, user):
        validated_data = set_numformat_validated_data(validated_data)
        with transaction.atomic():
           
            numformat_obj = super(UtilityServiceNumberFormatSerializer, self).update(instance, validated_data)
            numformat_obj.updated_by = user.id
            numformat_obj.updated_date = datetime.utcnow()
            numformat_obj.save()
            return numformat_obj
           

class UtilityServiceNumberFormatListSerializer(serializers.ModelSerializer):
    sub_module = SubModuleShortViewSerializer(source="get_sub_module_by_id")
    is_prefix = serializers.SerializerMethodField(method_name='conversion_bool')
    class Meta:
        model = UtilityServiceNumberFormatTbl
        fields = ('id_string','tenant','utility','prefix','startingno','currentno','is_prefix','sub_module')
    
    def conversion_bool(self, instance):
        if instance.is_prefix == True:
            return "YES"
        else:
            return "NO"

class UtilityServiceNumberFormatViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    sub_module = SubModuleShortViewSerializer(source="get_sub_module_by_id")
    is_prefix = serializers.SerializerMethodField(method_name='conversion_bool')

    class Meta:
        model = UtilityServiceNumberFormatTbl
        fields = ('id_string','tenant','tenant_id_string','utility','utility_id_string','sub_module','prefix','startingno','currentno','is_prefix')
    
    def conversion_bool(self, instance):
        if instance.is_prefix == True:
            return "YES"
        else:
            return "NO"



