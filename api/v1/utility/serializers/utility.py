__author__ = "aki"

from django.db import transaction
from rest_framework import serializers
from v1.utility.models.utility_master import UtilityMaster as UtilityMasterTbl


class UtilityMasterViewSerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = UtilityMasterTbl
        fields = ('id_string', 'tenant_name', 'short_name', 'name', 'phone_no', 'email_id')


class UtilityMasterSerializer(serializers.ModelSerializer):
    pass

    # class Meta:
    #     model = UtilityMasterTbl
    #     fields = ('id_string', 'tenant_name', 'short_name', 'name', 'phone_no', 'email_id')
    #
    # def create(self, validated_data, user):
    #     with transaction.atomic():
    #         project_team=[]
    #         if 'project_team' in validated_data:
    #             project_team = validated_data.pop('project_team')
    #
    #         project = super(ProjectSerializer, self).create(validated_data)
    #         project.project_owner = user.user
    #         project.created_by = user.username
    #         project.save()
    #         for team in project_team:
    #             team['project'] = project
    #             team['created_by'] = user.username
    #             team = Team.objects.create(**team)
    #         return project