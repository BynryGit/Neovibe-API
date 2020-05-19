__author__ = "Arpita"

from rest_framework import serializers

from v1.userapp.models.privilege import Privilege


class PrivilegeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Privilege
        depth = 1
        fields = ('id_string', 'tenant', 'utility', 'name', 'created_date')