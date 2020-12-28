from rest_framework import serializers
from v1.work_order.models.material_name import MaterialName as MaterialNameTbl
from v1.work_order.serializers.material_type import MaterialTypeListSerializer
from v1.work_order.serializers.material_subtype import MaterialSubTypeListSerializer


class MaterialNameListSerializer(serializers.ModelSerializer):
    material_subtype = MaterialSubTypeListSerializer(source="get_material_subtype")

    class Meta:
        model = MaterialNameTbl
        fields = ('name', 'id_string', 'material_subtype')
