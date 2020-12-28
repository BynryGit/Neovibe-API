from v1.utility.models.utility_master import get_utility_by_id_string
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.asset.models.asset_master import get_asset_by_id_string
from v1.work_order.models.work_order_master import get_work_order_master_by_id_string
from v1.work_order.models.work_order_rules import get_work_order_rule_by_id_string
from v1.work_order.models.service_appointment_status import get_service_appointment_status_by_id_string
from v1.utility.models.utility_services_number_format import UtilityServiceNumberFormat
import os
from rest_framework import status
from v1.commonapp.models.sub_module import get_sub_module_by_key

if os.environ['smart360_env'] == 'dev':
    from api.settings_dev import SECRET_KEY
else:
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



def set_service_appointment_validated_data(validated_data):
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

    if "consumer_id" in validated_data:
        consumers = get_consumer_by_id_string(validated_data["consumer_id"])
        if consumers:
            validated_data["consumer_id"] = consumers.id
        else:
            raise CustomAPIException("Consumer not found.", status_code=status.HTTP_404_NOT_FOUND)

    if "asset_id" in validated_data:
        asset = get_asset_by_id_string(validated_data["asset_id"])
        if asset:
            validated_data["asset_id"] = asset.id
        else:
            raise CustomAPIException("Asset not found.", status_code=status.HTTP_404_NOT_FOUND)

    if "service_id" in validated_data:
        service = get_work_order_master_by_id_string(validated_data["service_id"])
        if service:
            validated_data["service_id"] = service.id
        else:
            raise CustomAPIException("Service not found.", status_code=status.HTTP_404_NOT_FOUND)

    if "status_id" in validated_data:
        status = get_service_appointment_status_by_id_string(validated_data["status_id"])
        if status:
            validated_data["status_id"] = status.id
        else:
            raise CustomAPIException("status not found.", status_code=status.HTTP_404_NOT_FOUND)

    # if "rule_id" in validated_data:
    #     rule = get_work_order_rule_by_id_string(validated_data["rule_id"])
    #     if rule:
    #         validated_data["rule_id"] = rule.id
    #     else:
    #         raise CustomAPIException("Service Rule not found.", status_code=status.HTTP_404_NOT_FOUND)
    return validated_data


# Function for generating service appointment number according to utility
def generate_service_appointment_no(service_appointment):
    try:
        format_obj = UtilityServiceNumberFormat.objects.get(tenant=service_appointment.tenant, utility=service_appointment.utility,
                                                          sub_module_id=get_sub_module_by_key("DISPATCHER"))
        if format_obj.is_prefix:
            sa_number = format_obj.prefix + str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        else:
            sa_number = str(format_obj.currentno + 1)
            format_obj.currentno = format_obj.currentno + 1
            format_obj.save()
        return sa_number
    except Exception as e:
        raise CustomAPIException("sa_number no generation failed.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)