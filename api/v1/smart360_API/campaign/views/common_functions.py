import jwt

from api.v1.smart360_API.campaign.models.compaign_master import CampaignMaster
from api.v1.smart360_API.smart360_API.settings import SECRET_KEY



def get_filtered_campaign(request, user):
    compaign = CampaignMaster.objects.filter(tenant_id=user.tenant_id,
                                                utility_id__in=user.data_access.all())
    if request.data['utillity']:
        compaign = compaign.objects.filter(utility_id=
                                                     request.data['utillity'])
    if request.data['category']:
        compaign = compaign.objects.filter(consumer_category_id=
                                                     request.data['category'])
    if request.data['sub_category']:
        compaign = compaign.objects.filter(sub_category_id=
                                                     request.data['sub_category'])
    if request.data['cam_group']:
        compaign = compaign.objects.filter(cam_group= request.data['cam_group'])

    if request.data['area']:
        compaign = compaign.objects.filter(area_id=
                                                     request.data['area'])
    if request.data['subarea']:
        compaign = compaign.objects.filter(subarea_id=
                                                     request.data['subarea'])
    if request.data['status']:
        compaign = compaign.objects.filter(status_id=
                                                     request.data['status'])
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