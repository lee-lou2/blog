from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from app.user.models import UserProfile
from app.user.v1.serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
