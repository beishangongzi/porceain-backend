import datetime

import jwt
from django.conf import settings
from django.core import exceptions
from jwt import ExpiredSignatureError, DecodeError, InvalidTokenError
from rest_framework.authentication import BaseAuthentication, CSRFCheck
from rest_framework.exceptions import AuthenticationFailed

from .. import models


class JwtQueryParamsAuthentication(BaseAuthentication):
    """
    get token
    """

    def authenticate(self, request):
        # token = request.COOKIES.get("token")
        # print(token)
        # print(request.headers)
        try:
            token = request.headers["Authorization"]
        except KeyError:
            raise AuthenticationFailed('Invalid payload string: must be a json object')
        print(token)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, "HS256")
        except ExpiredSignatureError as e:
            raise AuthenticationFailed({"code": 200, "error": "expired token"})
        except DecodeError as e:
            raise AuthenticationFailed({'code': 2000, "error": "error token"})
        except InvalidTokenError as e:
            raise AuthenticationFailed({"code": 2000, "error": "illegal token"})
        user = models.User.objects.get(pk=payload['id'])
        if not user or not user.is_active:
            return None
        return user, token

    def create_token(self, payload: dict, expires_time: dict):
        header = {
            'typ': "jwt",
            'alg': "HS256"
        }
        payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(**expires_time)
        print(payload)

        result = jwt.encode(payload=payload,
                            key=settings.SECRET_KEY,
                            algorithm="HS256",
                            headers=header)
        return result





class MySessionAuthentication(BaseAuthentication):
    """
    Use Django's session framework for authentication.
    """

    def authenticate(self, request):
        """
        Returns a `User` if the request session currently has a logged in user.
        Otherwise returns `None`.
        """

        # Get the session-based user from the underlying HttpRequest object
        user = getattr(request._request, 'user', None)

        # Unauthenticated, CSRF validation not required
        if not user or not user.is_active:
            return None

        self.enforce_csrf(request)

        # CSRF passed with authenticated user
        return (user, None)

    def enforce_csrf(self, request):
        """
        Enforce CSRF validation for session based authentication.
        """

        def dummy_get_response(request):  # pragma: no cover
            return None

        check = CSRFCheck(dummy_get_response)
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
