from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password

from apis.authorization.models import User
from apis.authorization.keycloak import FMKeycloakAdmin

# Create your views here.

class AddUserView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            
            if not username or not email or not password:
                return Response(
                    {"error": "Username, email and password are required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                return Response(
                    {"error": "Username already exists"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            payload = {
                "username": username,
                "email": email,
                "password": password
            }
            
            # Create user in Keycloak
            keycloak_admin = FMKeycloakAdmin()
            kc_user_id = keycloak_admin.create_keycloak_user(payload)

            # Create user in Django
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(None),
                keycloak_id=kc_user_id
            )

            return Response(
                {"message": "User created successfully", "user_id": user.id},
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
