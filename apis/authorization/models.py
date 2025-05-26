from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    keycloak_id = models.CharField(max_length=64, blank=True, null=True, unique=True)

    # objects = KeycloakUserManager()