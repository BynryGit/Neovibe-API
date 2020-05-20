__author__ = "aki"

from rest_framework.exceptions import APIException
from api.messages import INVALID_TOKEN, UNAUTHORIZED_USER


class InvalidTokenException(APIException):
    status_code = 401
    default_detail = INVALID_TOKEN


class InvalidAuthorizationException(APIException):
    status_code = 403
    default_detail = UNAUTHORIZED_USER
