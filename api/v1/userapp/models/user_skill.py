import uuid
from datetime import datetime

from django.db import models

# from master.models import get_user_by_id_string
from v1.commonapp.models.skills import get_skill_by_id_string, get_skill_by_id
from v1.tenant.models.tenant_master import TenantMaster
from master import models as userModel

class UserSkill(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    user_id = models.BigIntegerField(null=True, blank=True)
    skill_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.tenant.name

    def __unicode__(self):
        return self.tenant.name

    def get_tenant(self):
        return self.tenant
    
    @property
    def get_skill(self):
        return get_skill_by_id(self.skill_id)
    
    @property
    def get_user(self):
        return userModel.get_user_by_id(self.user_id)


def get_skill_by_user_id(user_id):
    return UserSkill.objects.filter(user_id=user_id, is_active=True)


def get_record_by_values(user_id_string, skill_id_string):
    user = userModel.get_user_by_id_string(user_id_string)
    skill = get_skill_by_id_string(skill_id_string)
    return UserSkill.objects.filter(user_id=user.id, skill_id=skill.id).last()
