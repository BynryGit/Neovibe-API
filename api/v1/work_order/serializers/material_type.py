from rest_framework import serializers
from v1.work_order.models.material_type import MaterialType as MaterialTypeTbl


class MaterialTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialTypeTbl
        fields = ('name', 'id_string')
