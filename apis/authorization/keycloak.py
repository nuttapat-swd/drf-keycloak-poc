from django.conf import settings
from keycloak.keycloak_admin import KeycloakAdmin
from keycloak import KeycloakOpenID

class DEMOKeycloakAdmin(KeycloakAdmin):

    def __init__(self):
        super().__init__(
            server_url=settings.KEYCLOAK.get('KEYCLOAK_URL', ''),
            username=settings.KEYCLOAK.get('KEYCLOAK_ADMIN_USERNAME', ''),
            password=settings.KEYCLOAK.get('KEYCLOAK_ADMIN_PASSWORD', ''),
            realm_name=settings.KEYCLOAK.get('KEYCLOAK_REALM', ''),
            client_id='admin-cli',
            user_realm_name=settings.KEYCLOAK.get('KEYCLOAK_ADMIN_REALM', 'master'),
            verify=True
        )
        
    def create_keycloak_user(self, payload):
        """
        Create a new user in Keycloak
        
        Args:
            payload (dict): User data including username, email, password
            
        Returns:
            str: Keycloak user ID
        """
        # Create user data
        user_data = {
            "username": payload["username"],
            "email": payload["email"],
            "enabled": True,
            "emailVerified": True,
            "credentials": [
                {
                    "type": "password",
                    "value": payload["password"],
                    "temporary": False
                }
            ]
        }
        
        # Add first name and last name if provided
        if "first_name" in payload:
            user_data["firstName"] = payload["first_name"]
        if "last_name" in payload:
            user_data["lastName"] = payload["last_name"]
            
        # Create user in Keycloak and get user ID
        return self.create_user(payload=user_data)


class DEMOKeycloakOpenID(KeycloakOpenID):

    def __init__(self):
        super().__init__(
            server_url=settings.KEYCLOAK.get('KEYCLOAK_URL', ''),
            client_id=settings.KEYCLOAK.get('KEYCLOAK_CLIENT_ID', ''),
            realm_name=settings.KEYCLOAK.get('KEYCLOAK_REALM', ''),
            client_secret_key=settings.KEYCLOAK.get('KEYCLOAK_CLIENT_SECRET', ''),
            verify=True
        )

    def get_user_info(self, token):
        """
        Get user info from Keycloak using the provided token
        
        Args:
            token (str): Access token
            
        Returns:
            dict: User information
        """
        return self.userinfo(token)