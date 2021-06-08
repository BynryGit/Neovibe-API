__author__ = "Arpita"

from rest_framework import serializers
from v1.commonapp.models.module import Module
from v1.commonapp.models.sub_module import get_sub_module_by_id
from v1.utility.models.utility_sub_module import get_utility_submodules_by_module_id


class ModuleShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id_string', 'name')


class ModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = ('name', 'id_string')


class CustomModuleShortViewSerializer(serializers.ModelSerializer):
    sub_modules = serializers.SerializerMethodField()

    def get_sub_modules(self, module):
        utility_sub_module_obj = get_utility_submodules_by_module_id(module.id)
        sub_module = []
        for submodule in utility_sub_module_obj:
            dict = {}
            sub_module_obj = get_sub_module_by_id(submodule.submodule_id)
            dict['id_string'] = str(sub_module_obj.id_string)
            dict['name'] = str(sub_module_obj.name)
            sub_module.append(dict)
        unique_submodule_list = [i for n, i in enumerate(sub_module) if i not in sub_module[n + 1:]]
        return unique_submodule_list

    class Meta:
        model = Module
        fields = ('id_string', 'name', 'sub_modules')