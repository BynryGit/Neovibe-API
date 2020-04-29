from rest_framework.views import APIView
from v1.commonapp.common_functions import is_token_valid, get_payload, get_user, is_authorized
from v1.commonapp.models.sub_module import get_sub_module_by_id
from v1.consumer.models.consumer_master import get_consumer_by_id_string
from v1.userapp.models.privilege import get_privilege_by_id


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

                    # Get consumer details
                    consumer = get_consumer_by_id_string(request.data["consumer_id_string"])
                    data = {
                        "id_string": consumer.id_string,
                        "tenant": consumer.tenant.id_string,
                        "utility": consumer.utility.id_string,
                        "consumer_no": "",
                        "first_name": "",
                        "middle_name": "",
                        "last_name": "",
                        "email_id": ""
                    }
        except Exception as e:
            pass