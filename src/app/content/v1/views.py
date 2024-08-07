from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from app.content.models import Content, ContentComment
from app.content.v1.serialziers import (
    ContentSerializer,
    ContentCommentSerializer,
)


class ContentViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_object(self):
        return super().get_object()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class ContentCommentViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):
    queryset = ContentComment.objects.all()
    serializer_class = ContentCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        content_id = self.kwargs.get("content_id")
        queryset = super().get_queryset()
        return queryset.filter(content_id=content_id).filter(parent__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
