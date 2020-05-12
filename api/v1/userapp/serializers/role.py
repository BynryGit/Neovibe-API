from rest_framework import serializers

from v1.userapp.models.role_status import RoleStatus
from v1.userapp.models.user_role import UserRole


class RoleStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoleStatus
        fields = ('status', 'id_string')


class RoleListSerializer(serializers.ModelSerializer):
    status = RoleStatusSerializer(many=False,required=True,source='get_role_status')
    role_type = serializers.ReadOnlyField(source='get_role_type')
    role_sub_type = serializers.ReadOnlyField(source='get_role_sub_type')
    form_factor = serializers.ReadOnlyField(source='get_form_factor')
    department = serializers.ReadOnlyField(source='get_department')

    class Meta:
        model = UserRole
        fields = ('id_string', 'name', 'role_type', 'role_sub_type', 'status', 'form_factor', 'department',
                  'created_on')