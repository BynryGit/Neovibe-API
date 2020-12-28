from rest_framework import serializers
from v1.work_order.models.material_subtype import MaterialSubType as MaterialSubTypeTbl
from v1.work_order.serializers.material_type import MaterialTypeListSerializer


class MaterialSubTypeListSerializer(serializers.ModelSerializer):
    material_type = MaterialTypeListSerializer(source="get_material_type")

    class Meta:
        model = MaterialSubTypeTbl
        fields = ('name', 'material_type', 'id_string')
