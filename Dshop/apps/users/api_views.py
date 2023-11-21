from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import CustomUser
from .serializers import RegistrationSerializer

User = get_user_model()


class RegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API Viewset responsible for single user registration

    :accepts: User model [username, email] + password1, password2
    :returns: 201 / 400
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    throttle_scope = 'registration'
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        custom_user = CustomUser(user=user)
        custom_user.save()
