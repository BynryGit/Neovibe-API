__author__ = "aki"

import requests
from v1.commonapp.views.logger import logger


def import_bill_distribution_data():
    try:
        url = ''
        url_response = requests.get(url)
        data = dict(url_response.json())
        if data['RESULT'] == 'SUCCESS':
            bill_distribution_obj = data['DATA']
            for bill_distribution in bill_distribution_obj:
                pass
        else:
            print("no data")
    except Exception as ex:
        print(ex)
        logger().log(ex, 'ERROR', )