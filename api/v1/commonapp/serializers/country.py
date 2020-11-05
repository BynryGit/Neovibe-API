__author__ = "aki"

from rest_framework import serializers
from v1.commonapp.models.country import Country as CountryTbl
from v1.consumer.views.common_functions import set_validated_data
from django.db import transaction



class CountryViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    
  

    class Meta:
        model = CountryTbl
        fields = ('__all__')

class CountrySerializer(serializers.ModelSerializer):
    # utility_id = serializers.CharField(required=False, max_length=200)
    # tenant_id = serializers.CharField(required=False, max_length=200)
    class Meta:
        model = CountryTbl
        fields = ('__all__')
    
    # def create(self, validated_data, user):
    #     # validated_data =  set_validated_data(validated_data)
    #     # with transaction.atomic():
    #     #     country_obj = super(CountrySerializer, self).create(validated_data)
    #     #     country_obj.created_by = user.id
    #     #     country_obj.save()
    #     #     return country_obj

class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryTbl
        fields = ('name', 'id_string','key')



