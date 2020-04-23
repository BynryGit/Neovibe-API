from api.v1.smart360_API.smart360_API.campaign.models.campaign_master import Campaign




def get_filtered_campaign(request, user):
    compaign = Campaign.objects.filter(tenant_id=user.tenant_id,
                                                utility_id__in=user.data_access.all())

    if request.data['cam_type_id']:
        compaign = compaign.objects.filter(type_id=request.data['cam_type_id'])

    if request.data['frequency_id']:
        compaign = compaign.objects.filter(frequency_id=request.data['frequency_id'])

    if request.data['category_id']:
        compaign = compaign.objects.filter(category_id=request.data['category_id'])

    if request.data['sub_category_id']:
        compaign = compaign.objects.filter(sub_category_id=request.data['sub_category_id'])

    if request.data['status_id']:
        compaign = compaign.objects.filter(status_id=request.data['status_id'])

    return compaign



