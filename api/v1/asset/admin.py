from django.contrib import admin
from v1.asset.models.asset_master import Asset
from v1.asset.models.asset_status import AssetStatus
from v1.asset.models.asset_amc_contract import AssetAmcContract
from v1.asset.models.asset_category import AssetCategory
from v1.asset.models.asset_sub_category import AssetSubCategory
from v1.asset.models.asset_insurance import AsssetInsurance
from v1.asset.models.asset_service_history import AssetServiceHistory
from v1.asset.models.asset_service_history_status import AssetServiceHistoryStatus
from v1.asset.models.resource_assign import ResourceAssign
from v1.asset.models.sop_assign import SopAssign
from v1.asset.models.transaction_type import TransactionType


admin.site.register(Asset)
admin.site.register(AssetStatus)
admin.site.register(AssetAmcContract)
admin.site.register(AssetCategory)
admin.site.register(AssetSubCategory)
admin.site.register(AsssetInsurance)
admin.site.register(AssetServiceHistory)
admin.site.register(AssetServiceHistoryStatus)
admin.site.register(ResourceAssign)
admin.site.register(SopAssign)
admin.site.register(TransactionType)
