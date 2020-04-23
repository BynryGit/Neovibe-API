import jwt

from api.v1.smart360_API.smart360_API.settings import SECRET_KEY
from api.v1.smart360_API.smart360_API.campaign.models.campaign_master import CampaignMaster

def get_filtered_campaign(request, user):
    compaign = CampaignMaster.objects.filter(tenant_id=user.tenant_id,
                                                utility_id__in=user.data_access.all())

    if request.data['cam_type']:
        compaign = compaign.objects.filter(type_id=request.data['cam_type_id'])

    if request.data['frequency']:
        compaign = compaign.objects.filter(frequency_id=request.data['frequency_id'])

    if request.data['category']:
        compaign = compaign.objects.filter(category_id=request.data['category_id'])

    if request.data['status']:
        compaign = compaign.objects.filter(status_id=request.data['status'])

    return compaign



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