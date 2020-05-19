__author__ = "Arpita"

from rest_framework import serializers

from v1.userapp.models.privilege import Privilege


class PrivilegeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Privilege
        depth = 1
        fields = ('id_string', 'tenant', 'utility', 'name', 'created_date')


# class PrivilegeSerializer(serializers.ModelSerializer):
#     type_id = serializers.CharField(required=False, max_length=200)
#     sub_type_id = serializers.CharField(required=False, max_length=200)
#     form_factor_id = serializers.CharField(required=False, max_length=200)
#     department_id = serializers.CharField(required=False, max_length=200)
#     role_ID = serializers.CharField(required=False, max_length=200)
#     role = serializers.CharField(required=False, max_length=200)
#
#     class Meta:
#         model = UserRole
#         fields = '__all__'
#
#     def create(self, validated_data, user):
#         validated_data =  set_validated_data(validated_data)
#         with transaction.atomic():
#             role_obj = super(RoleSerializer, self).create(validated_data)
#             role_obj.created_by = user.id
#             role_obj.created_date = datetime.utcnow()
#             role_obj.tenant = user.tenant
#             role_obj.utility = user.utility
#             role_obj.is_active = True
#             role_obj.save()
#             return role_obj
#
#     def update(self, instance, validated_data, user):
#         validated_data = set_validated_data(validated_data)
#         with transaction.atomic():
#             role_obj = super(RoleSerializer, self).update(instance, validated_data)
#             role_obj.updated_by = user.id
#             role_obj.updated_date = datetime.utcnow()
#             role_obj.save()
#             return role_obj


class PrivilegeViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Privilege
        depth = 1
        fields = ('id_string', 'tenant', 'utility', 'name', 'created_date', 'is_active')
