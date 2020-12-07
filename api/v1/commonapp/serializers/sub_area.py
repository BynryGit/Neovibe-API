from rest_framework import serializers, status
from api.settings import DISPLAY_DATE_TIME_FORMAT
from v1.commonapp.models.sub_area import SubArea as SubAreaTbl
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.utility.serializers.utility import UtilitySerializer
from v1.commonapp.serializers.area import AreaListSerializer
from datetime import datetime
from django.db import transaction
from api.messages import SUBAREA_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.common_functions import set_subarea_validated_data


class SubAreaViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    area = AreaListSerializer(many="False", source="get_area")

    class Meta:
        model = SubAreaTbl
        fields = (
            'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'id_string', 'area')


class SubAreaSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    area_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = SubAreaTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_subarea_validated_data(validated_data)
            if SubAreaTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                         utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(SUBAREA_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                subarea_obj = super(SubAreaSerializer, self).create(validated_data)
                subarea_obj.created_by = user.id
                subarea_obj.updated_by = user.id
                subarea_obj.save()
                return subarea_obj

    def update(self, instance, validated_data, user):
        validated_data = set_subarea_validated_data(validated_data)
        with transaction.atomic():
            subarea_obj = super(SubAreaSerializer, self).update(instance, validated_data)
            subarea_obj.updated_by = user.id
            subarea_obj.updated_date = datetime.utcnow()
            subarea_obj.save()
            return subarea_obj


class SubAreaListSerializer(serializers.ModelSerializer):
    area = AreaListSerializer(source="get_area")

    class Meta:
        model = SubAreaTbl
        fields = ('name', 'id_string', 'area')
