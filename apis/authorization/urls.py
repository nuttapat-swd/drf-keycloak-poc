from django.urls import path
from .views import AddUserView

urlpatterns = [
    path('users/', AddUserView.as_view(), name='add_user'),
]