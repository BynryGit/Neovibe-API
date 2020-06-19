__author__ = "aki"

import requests
from v1.commonapp.views.logger import logger
from v1.meter_reading.models.consumer import Consumer
from v1.meter_reading.models.route import Route


def import_bill_distribution_data():
    try:
        url = ''
        url_response = requests.get(url)
        data = dict(url_response.json())
        if data['RESULT'] == 'SUCCESS':
            bill_distribution_obj = data['DATA']
            for bill_distribution in bill_distribution_obj:
                bill_distribution_route = Route.objects.filter(month=bill_distribution['BILL_MONTH'], token=bill_distribution['token']).exists()
                if bill_distribution_route:
                    pass
                else:
                    bill_distribution_route = Route(
                        month=bill_distribution['BILL_MONTH'],
                        token=bill_distribution['token'],
                        is_bill_distribution=True
                    )
                    bill_distribution_route.save()
                bill_distribution_consumer = Consumer.objects.filter(route_id=bill_distribution_route.id,
                                                                     consumer_no=bill_distribution['consumer_no'],
                                                                     month=bill_distribution['BILL_MONTH']).exists()
                if bill_distribution_consumer:
                    pass
                else:
                    Consumer(
                        route_id=bill_distribution_route.id,
                        consumer_no = bill_distribution['consumer_no'],
                        month=bill_distribution['BILL_MONTH'],
                        is_bill_distribution=True
                    ).save()
        else:
            print("no data")
    except Exception as ex:
        print(ex)
        logger().log(ex, 'ERROR', )