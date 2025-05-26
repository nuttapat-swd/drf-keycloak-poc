# from django.contrib.auth import get_user_model
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from apis.authorization.keycloak import FMKeycloakAdmin

# User = get_user_model()

# @receiver(post_save, sender=User)
# def set_unusable_password_on_create(sender, instance, created, **kwargs):
#     if created and not instance.has_usable_password():
#         instance.set_unusable_password()
#         instance.save()
#         kc_user = FMKeycloakAdmin.create_user()


