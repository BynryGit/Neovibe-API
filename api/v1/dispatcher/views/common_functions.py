
from v1.commonapp.models.service_type import get_service_type_by_id_string
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.dispatcher.models.sop_status import get_sop_status_by_id_string
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.asset.models.asset_master import get_asset_by_id_string
from v1.supplier.models.supplier import get_supplier_by_id_string
from v1.dispatcher.models.service_appointments import get_service_request_by_id_string
def is_data_verified(request):
    return True

def set_validated_data(validated_data):
    if "service_request_id" in validated_data:
        service_request_id = get_service_request_by_id_string(validated_data["service_request_id"])
        validated_data["service_request_id"] = service_request_id.id

    if "service_type_id" in validated_data:
        survey_type = get_service_type_by_id_string(validated_data["service_type_id"])
        validated_data["service_type_id"] = survey_type.id

    if "asset_id" in validated_data:
        asset_id = get_asset_by_id_string(validated_data["asset_id"])
        validated_data["asset_id"] = asset_id.id

    if "city_id" in validated_data:
        city_id = get_city_by_id_string(validated_data["city_id"])
        validated_data["city_id"] = city_id.id

    if "area_id" in validated_data:
        area = get_area_by_id_string(validated_data["area_id"])
        validated_data["area_id"] = area.id

    if "sub_area_id" in validated_data:
        sub_area = get_sub_area_by_id_string(validated_data["sub_area_id"])
        validated_data["sub_area_id"] = sub_area.id

    if "consumer_id" in validated_data:
        consumer_id = get_consumer_by_id_string(validated_data["consumer_id"])
        validated_data["consumer_id"] = consumer_id.id

    if "status_id" in validated_data:
        status_id = get_sop_status_by_id_string(validated_data["status_id"])
        validated_data["status_id"] = status_id.id

    if "vendor_id" in validated_data:
        vendor_id = get_supplier_by_id_string(validated_data["vendor_id"])
        validated_data["vendor_id"] = vendor_id.id

    return validated_data

