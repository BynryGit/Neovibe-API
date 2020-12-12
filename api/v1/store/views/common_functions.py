from rest_framework import status
from v1.store.models.store_type import get_store_type_by_id_string
from api.messages import UTILITY_NOT_FOUND,TENANT_NOT_FOUND 
from v1.tenant.models.tenant_state import get_tenant_state_by_id_string
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.models.tenant_master import get_tenant_by_id_string

def set_store_type_vaidated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException(UTILITY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException(TENANT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    return validated_data