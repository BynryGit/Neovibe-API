__author__ = "aki"

from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from api.messages import *


class InvalidTokenException(APIException):
    status_code = 401
    default_detail = INVALID_TOKEN


class InvalidAuthorizationException(APIException):
    status_code = 403
    default_detail = UNAUTHORIZED_USER


class ObjectNotFoundException(APIException):
    status_code = 404
    default_detail = DATA_NOT_EXISTS


class CustomAPIException(ValidationError):
    """
    raises API exceptions with custom messages and custom status codes
    """
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code
