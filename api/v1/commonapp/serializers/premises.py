from rest_framework import serializers, status
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.models.premises import Premise as PremiseTbl
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.utility.serializers.utility import UtilitySerializer
from v1.commonapp.serializers.area import AreaListSerializer
from v1.commonapp.serializers.sub_area import SubAreaListSerializer
from v1.commonapp.serializers.zone import ZoneListSerializer
from v1.commonapp.serializers.city import CityListSerializer
from v1.commonapp.serializers.state import StateListSerializer
from v1.commonapp.serializers.country import CountryListSerializer
from v1.commonapp.serializers.region import RegionListSerializer
from datetime import datetime
from django.db import transaction
from api.messages import PREMISE_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.common_functions import set_premise_validated_data
from v1.commonapp.serializers.sub_area import SubAreaListSerializer
from v1.commonapp.models.area import get_area_by_id


class PremisesShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiseTbl
        fields = ('id_string', 'name')


class PremiseViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    subarea = SubAreaListSerializer(source="get_sub_area")

    class Meta:
        model = PremiseTbl
        fields = (
            'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'id_string', 'subarea')


class PremiseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    subarea_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = PremiseTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_premise_validated_data(validated_data)
            if PremiseTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                         utility_id=validated_data['utility_id'],subarea_id=validated_data['subarea_id']).exists():
                raise CustomAPIException(PREMISE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                premise_obj = super(PremiseSerializer, self).create(validated_data)
                premise_obj.created_by = user.id
                premise_obj.updated_by = user.id
                premise_obj.save()
                return premise_obj

    def update(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_premise_validated_data(validated_data)
            if PremiseTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                         utility_id=validated_data['utility_id'],subarea_id=validated_data['subarea_id']).exists():
                raise CustomAPIException(PREMISE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                premise_obj = super(PremiseSerializer, self).update(validated_data)
                premise_obj.created_by = user.id
                premise_obj.updated_by = user.id
                premise_obj.save()
                return premise_obj



class PremiseListSerializer(serializers.ModelSerializer):
    subarea = SubAreaListSerializer(source="get_sub_area")

    class Meta:
        model = PremiseTbl
        fields = ('name', 'id_string','subarea','GIS','MRU')