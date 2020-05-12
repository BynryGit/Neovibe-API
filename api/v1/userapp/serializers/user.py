from rest_framework import serializers

from v1.userapp.models.user_master import UserDetail
from v1.userapp.models.user_status import UserStatus


class UserStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStatus
        fields = ('status', 'id_string')


class UserListSerializer(serializers.ModelSerializer):
    status = UserStatusSerializer(many=False,required=True,source='get_user_status')
    department = serializers.ReadOnlyField(source='get_department')
    role = serializers.ReadOnlyField(source='get_user_role')

    class Meta:
        model = UserDetail
        fields = ('id_string', 'name', 'user_ID', 'contact', 'status', 'email', 'department',
                  'role')