import django_filters
from rest_framework import viewsets, mixins, response, pagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.content.models import Content, ContentComment, ContentLike
from app.content.v1.filters import ContentFilter
from app.content.v1.serialziers import (
    ContentSerializer,
    ContentCommentSerializer,
    ContentLikeSerializer,
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
    pagination_class = pagination.LimitOffsetPagination
    filterset_class = ContentFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ["create", "update", "partial_update"]:
            return queryset.filter(user=self.request.user)
        return queryset

    def get_object(self):
        return super().get_object()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        resp = super().retrieve(request, *args, **kwargs)
        content = self.get_object()
        content.view_count += 1
        content.save()
        return resp

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @action(detail=True, methods=["PUT"], serializer_class=ContentLikeSerializer)
    def like(self, request, *args, **kwargs):
        content = self.get_object()
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, content=content)
        return response.Response(data=serializer.data)


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
