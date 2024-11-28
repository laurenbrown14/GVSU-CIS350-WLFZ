import jwt
from django.conf import settings
from .models import User
from datetime import datetime, timedelta
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header


class LoginManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LoginManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def authenticate(self, email, password):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return self.generate_token(user)
        except User.DoesNotExist:
            return None

    def generate_token(self, user):
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=1),  # Token expires in 1 hour
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

    def validate_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            # Ensure the user exists in the database
            user = User.objects.get(id=user_id)
            return user
            # return User.objects.get(id=payload['user_id'])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            raise AuthenticationFailed('Invalid or expired token')

    @staticmethod
    def get_user_from_request(request):
        # If user is already attached to the request by the middleware, return it
        if hasattr(request, 'user'):
            return request.user
        raise AuthenticationFailed('User not authenticated')
