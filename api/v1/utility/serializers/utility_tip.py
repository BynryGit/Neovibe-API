from rest_framework import serializers
from v1.utility.models.utility_tip import UtilityTip as UtilityTipTbl
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import TIP_ALREADY_EXIST
from v1.utility.views.common_functions import set_tip_validated_data
from rest_framework import status


class UtilityTipListSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = UtilityTipTbl
        fields = ('id_string', 'tenant', 'tenant_id_string', 'utility', 'utility_id_string', "tip", "description", 'created_date')


class UtilityTipViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = UtilityTipTbl
        fields = (
            'id_string', 'tenant', 'tenant_id_string', 'utility', "tip", "description", 'utility_id_string')


class UtilityTipSerializer(serializers.ModelSerializer):
    tip = serializers.CharField(required=True, max_length=200,
                                error_messages={"required": "The field Tip is required."})
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = UtilityTipTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_tip_validated_data(validated_data)
            if UtilityTipTbl.objects.filter(tip=validated_data['tip'], tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(TIP_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                utility_tip_obj = super(UtilityTipSerializer, self).create(validated_data)
                utility_tip_obj.created_by = user.id
                utility_tip_obj.save()
                return utility_tip_obj

    def update(self, instance, validated_data, user):
        validated_data = set_tip_validated_data(validated_data)
        if UtilityTipTbl.objects.filter(tip=validated_data['tip'], tenant_id=validated_data['tenant_id'],
                                        utility_id=validated_data['utility_id']).exists():
            raise CustomAPIException(TIP_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                utility_tip_obj = super(UtilityTipSerializer, self).update(instance, validated_data)
                utility_tip_obj.updated_by = user.id
                utility_tip_obj.updated_date = datetime.utcnow()
                utility_tip_obj.save()
                return utility_tip_obj
