from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.views.logger import logger
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.commonapp.models.service_type import get_service_type_by_id_string
from v1.commonapp.models.service_sub_type import get_service_sub_type_by_id_string
import jwt  # jwt token library
from rest_framework import status
from api.settings import SECRET_KEY





def set_work_order_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException("Utility not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "tenant_id" in validated_data:
        tenant = get_tenant_by_id_string(validated_data["tenant_id"])
        if tenant:
            validated_data["tenant_id"] = tenant.id
        else:
            raise CustomAPIException("Tenant not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "service_type_id" in validated_data:
        service_type = get_service_type_by_id_string(validated_data["service_type_id"])
        if service_type:
            validated_data["service_type_id"] = service_type.id
        else:
            raise CustomAPIException("Service type not found.", status_code=status.HTTP_404_NOT_FOUND)
    if "service_subtype_id" in validated_data:
        service_subtype = get_service_sub_type_by_id_string(validated_data["service_subtype_id"])
        if service_subtype:
            validated_data["service_subtype_id"] = service_subtype.id
        else:
            raise CustomAPIException("Service Subtype not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data