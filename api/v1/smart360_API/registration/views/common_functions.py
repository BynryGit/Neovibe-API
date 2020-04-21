import jwt

from api.v1.smart360_API.registration.models.consumer_registration import ConsumerRegistration
from api.v1.smart360_API.smart360_API.settings import SECRET_KEY



def get_filtered_registrations(request, user):
    registrations = ConsumerRegistration.objects.filter(tenant_id=user.tenant_id,
                                                utility_id__in=user.data_access.all())
    if request.data['utillity']:
        registrations = registrations.objects.filter(utility_id=
                                                     request.data['utillity'])
    if request.data['category']:
        registrations = registrations.objects.filter(consumer_category_id=
                                                     request.data['category'])
    if request.data['sub_category']:
        registrations = registrations.objects.filter(sub_category_id=
                                                     request.data['sub_category'])
    if request.data['city']:
        registrations = registrations.objects.filter(city_id=
                                                     request.data['city'])
    if request.data['area']:
        registrations = registrations.objects.filter(area_id=
                                                     request.data['area'])
    if request.data['subarea']:
        registrations = registrations.objects.filter(subarea_id=
                                                     request.data['subarea'])
    if request.data['status']:
        registrations = registrations.objects.filter(status_id=
                                                     request.data['status'])
    return registrations

def is_token_valid(token):
    return Token.objects.filter(token=token).exists()

def get_payload(token):
    return jwt.decode(token, SECRET_KEY, algorithms='RS256')

def get_user(id_string):
    user = User.objects.get(id_string = id_string)
    return user

def check_authorization(user, privillege, sub_module):
    privilleges = user.privilleges.all()
    sub_modules = user.sub_modules.all()
    if privillege in privilleges:
        if sub_module in sub_modules:
            return True
    else:
        return False