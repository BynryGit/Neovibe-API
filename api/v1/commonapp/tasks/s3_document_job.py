__author__ = "chinmay"

# API Header
# Package: Basic
# Modules: All
# Sub Module: All
# Usage: This task is used to update the auth details, auth time span data
# Tables used: Documents (CommonApp)
# Author: Chinmay
# Created on: 26/04/2021

from v1.commonpp.models.document import Document
from v1.commonapp.views.logger import logger
from datetime import datetime, timedelta


def document_details_update():
    try:
        document_obj = Document.objects.filter(last_auth_generated__lte=datetime.now() - timedelta(days=7),
                                               is_active=True).update(document_auth_details=None, auth_time_span=None)
    except Exception as ex:
        print(ex)
        logger().log(ex, 'MEDIUM', module='ADMIN', sub_module='SYSTEM CONFIGURATION')


document_details_update()
