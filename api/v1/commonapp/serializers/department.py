from rest_framework import serializers

from v1.commonapp.models.department import Department


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('status', 'id_string')