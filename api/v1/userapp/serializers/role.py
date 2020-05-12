from rest_framework import serializers
from v1.userapp.models.user_role import UserRole


class RoleListSerializer(serializers.ModelSerializer):
    role_type = serializers.ReadOnlyField(source='get_role_type')
    role_sub_type = serializers.ReadOnlyField(source='get_role_sub_type')
    status = serializers.ReadOnlyField(source='get_role_status')
    form_factor = serializers.ReadOnlyField(source='get_form_factor')
    department = serializers.ReadOnlyField(source='get_department')

    class Meta:
        model = UserRole
        fields = ('id_string', 'name', 'role_type', 'role_sub_type', 'status', 'form_factor', 'department',
                  'created_on')