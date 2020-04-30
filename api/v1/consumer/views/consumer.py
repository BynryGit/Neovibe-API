from rest_framework.views import APIView
from v1.common  app.common_functions import is_token_valid, get_payload, get_user, is_authorized
from v1.commonapp.models.area import get_area_by_id
from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.models.consumer_category import get_consumer_category_by_id
from v1.commonapp.models.consumer_sub_category import get_consumer_sub_category_by_id
from v1.commonapp.models.country import get_country_by_id
from v1.commonapp.models.state import get_state_by_id
from v1.commonapp.models.sub_area import get_sub_area_by_id
from v1.commonapp.models.sub_module import get_sub_module_by_id
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.consumer.models.consumer_scheme_master import get_scheme_by_id
from v1.meter_reading.models.bill_cycle import get_bill_cycle_by_id
from v1.userapp.models.privilege import get_privilege_by_id
from v1.utility.models.utility_service_plan import get_utility_service_plan_by_id


class ConsumerApiView(APIView):
    def get(self, request, format=None):
        try:
            # Checking authentication start
            if is_token_valid(request.data['token']):
                payload = get_payload(request.data['token'])
                user = get_user(payload['id_string'])
            # Checking authentication end

                # Checking authorization start
                privilege = get_privilege_by_id(1)
                sub_module = get_sub_module_by_id(1)
                if is_authorized(user, privilege, sub_module):
                # Checking authorization end

                    # Get consumer details and lookups
                    consumer = get_consumer_by_id_string(request.data["consumer_id_string"])
                    country = get_country_by_id(consumer.country)
                    state = get_state_by_id(consumer.state)
                    city = get_city_by_id(consumer.city)
                    cycle = get_bill_cycle_by_id(consumer.cycle)
                    area = get_area_by_id(consumer.area)
                    sub_area = get_sub_area_by_id(consumer.sub_area)
                    scheme = get_scheme_by_id(consumer.scheme)
                    category = get_consumer_category_by_id(consumer.category)
                    sub_category = get_consumer_sub_category_by_id(consumer.sub_category)
                    utility_service_plan = get_utility_service_plan_by_id(consumer.utility_service_plan)
                    data = {
                        "id_string": consumer.id_string,
                        "tenant": consumer.tenant.id_string,
                        "utility": consumer.utility.id_string,
                        "consumer_no": consumer.cosumer_no,
                        "first_name": consumer.first_name,
                        "middle_name": consumer.middle_name,
                        "last_name": consumer.last_name,
                        "email_id": consumer.email_id,
                        "phone_mobile": consumer.phone_mobile,
                        "phone_landline": consumer.phone_landline,
                        "address_line_1": consumer.address_line_1,
                        "street": consumer.street,
                        "zipcode": consumer.zipcode,
                        "country_id_string": country.id_string,
                        "city_id_string": city.id_string,
                        "state_id_string": state.id_string,
                        "cycle_id_string": cycle.id_string,
                        "area_id_string": area.id_string,
                        "sub_area_id_string": sub_area.id_string,
                        "route": "",
                        "scheme": scheme.id_string,
                        "deposit_amt": consumer.deposit_amt,
                        "collected_amt": consumer.collected_amt,
                        "category_id_string": category.id_string,
                        "sub_category_id_string": sub_category.id_string,
                        "utility_service_plan_id_string": utility_service_plan.id_string,
                        "is_vip": consumer.is_vip,
                        "is_connectivity": consumer.is_connectivty
                    }
        except Exception as e:
            pass