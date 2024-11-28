from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.urls import resolve  # To resolve the current URL
from .auth_manager import LoginManager

class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Define URLs that should not require authentication
        unauthenticated_paths = [
            'login',  # Adjust this based on your URL path
            'signup',  # Adjust this based on your URL path
        ]

        # Get the current URL path name
        current_url_name = resolve(request.path_info).url_name

        # Skip authentication for specific URLs (e.g., login and signup)
        if current_url_name in unauthenticated_paths:
            return None

        # Get the authorization header
        auth_header = request.headers.get('Authorization')

        if auth_header:
            # Split the Bearer and the actual token
            try:
                token_type, token = auth_header.split(' ')
                if token_type.lower() != 'bearer':
                    raise ValueError("Invalid token type")
            except ValueError:
                return JsonResponse({'error': 'Invalid Authorization header format'}, status=401)

            # Validate token and set user to request
            try:
                user = LoginManager().validate_token(token)
                request.user = user
                request.auth_token = token  # Store the token for further use
                return None
            except:
                return JsonResponse({'error': 'Invalid or expired token'}, status=401)

        # Return unauthorized response if not authenticated and not in unauthenticated paths
        return JsonResponse({'error': 'Unauthorized'}, status=401)
