import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# table header
# table type : lookup
# table name : 2.12.7 Wage Cycle
# table description : It will be used in the soucing module in setting. Wage Cycle and ID used to Various operator Or Utility
# frequency of data changes : Low
# sample tale data :
# reference tables :
# auther : Saloni

# change history
# 22/04/2020 Creation Saloni


class WageCycle(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    wage_cycle_name = models.CharField(max_length=200, blank=False, null=False)
    created_by = models.CharField(blank=False, null=False)
    updated_by = models.CharField(blank=False, null=False)
    created_date = models.DateField(default=datetime.now)
    updated_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.wage_cycle_name
