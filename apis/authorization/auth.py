# your_project/auth.py

from pprint import pprint
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apis.authorization.keycloak import DEMOKeycloakOpenID

User = get_user_model()
keycloak_openid = DEMOKeycloakOpenID()

class KeycloakAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth = request.headers.get('Authorization', None)
        if not auth or not auth.startswith("Bearer "):
            return None

        token = auth.split(" ")[1]
        try:
            # Validate the token
            token_info = keycloak_openid.introspect(token)
            if not token_info.get('active'):
                return None
                # raise AuthenticationFailed("Token is not active")

            # Optionally decode token to get claims
            userinfo = keycloak_openid.userinfo(token)
            username = userinfo.get('preferred_username')
            email = userinfo.get('email', '')

            if not username:
                return None
                # raise AuthenticationFailed("Username missing in token claims")

        except Exception as e:
            raise AuthenticationFailed(f"Token validation failed: {str(e)}")

        # Create or get Django user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email}
        )
        if created:
            user.set_unusable_password()
            user.save()

        return (user, None)
