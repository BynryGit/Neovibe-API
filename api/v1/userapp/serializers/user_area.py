from rest_framework import serializers

from v1.commonapp.serializers.area import GetAreaSerializer
from v1.userapp.models.user_area import UserArea


class UserAreaSerializer(serializers.ModelSerializer):
    area = GetAreaSerializer(many=False, required=True, source='get_area')

    class Meta:
        model = UserArea
        fields = ('area',)
