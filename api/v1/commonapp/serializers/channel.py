from rest_framework import serializers, status
from v1.commonapp.models.channel import Channel as ChannelTbl
from v1.commonapp.views.custom_exception import CustomAPIException
from datetime import datetime
from api.messages import CHANNEL_ALREADY_EXIST
from datetime import datetime
from django.db import transaction
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.common_functions import set_channel_validated_data
from v1.utility.models.utility_payment_channel import UtilityPaymentChannel as UtilityPaymentChannelTbl


class ChannelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelTbl
        fields = '__all__'


class ChannelViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = UtilityPaymentChannelTbl
        fields = '__all__'


class ChannelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    channel_id = serializers.CharField(required=True, max_length=200)


    class Meta:
        model = UtilityPaymentChannelTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_channel_validated_data(validated_data)
            if UtilityPaymentChannelTbl.objects.filter(name=validated_data['name'],
                                                       tenant_id=validated_data['tenant_id'],
                                                       utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(CHANNEL_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                channel_obj = super(ChannelSerializer, self).create(validated_data)
                channel_obj.created_by = user.id
                channel_obj.save()
                return channel_obj
